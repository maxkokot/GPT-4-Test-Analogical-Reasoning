import os
import re
import pandas as pd
import openai
from collections import defaultdict
import logging
import click
from dotenv import load_dotenv, find_dotenv

from data.data import load_config, read_txt_info, \
    read_hum_answers, write_answers
from gpt_requests.gpt_requests import ask_gpt4


def prepare_questions(ph2ans_dir, ph1que_dir, gptque_dir,
                      selected_idxs):
    lst_files = os.listdir(ph2ans_dir)
    lst_data_dfs = []
    pairs_desc_subcat = {}

    for file_name in lst_files:

        # reading answers provived by humans
        # on the questions related to
        # current subcategory
        idx = re.findall('[0-9]+[a-z]', file_name)[0]
        ans_name = f"Phase2Answers-{idx}.txt"
        ans_path = os.path.join(ph2ans_dir, ans_name)

        df = read_hum_answers(ans_path)
        df['file_idx'] = idx
        lst_data_dfs.append(df)

        # reading pairs describing
        # current subcategory
        q_name = f"Phase1Questions-{idx}.txt"
        q_path = os.path.join(ph1que_dir, q_name)
        q_txt = read_txt_info(q_path)

        # remove correct answer
        q_pairs = re.findall('[a-z]+:[a-z]+', q_txt)
        q_pairs = ', '.join(q_pairs)
        pairs_desc_subcat[idx] = q_pairs

    data = pd.concat(lst_data_dfs).reset_index(drop=True)

    # extracting small subset

    data = data[data['file_idx'].isin(selected_idxs)]
    pairs_desc_subcat = {idx: pairs for idx, pairs in
                         pairs_desc_subcat.items()
                         if idx in selected_idxs}

    # remove duplicates, leave unique options only
    # we need at least one human answer for each question
    # in order to formulate the questions fo GPT4

    options_df = data[['file_idx', 'pair1', 'pair2', 'pair3', 'pair4']]
    options_df = options_df.drop_duplicates()
    options_df['describing_pairs'] = options_df['file_idx'].\
        map(pairs_desc_subcat)

    options_df.to_csv(os.path.join(gptque_dir, 'questions_to_gpt4.csv'),
                      index=False)

    return options_df


def send_questions(options_df, q_template):

    # this loads your open api key from .env file
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # receive GPT-4 answers
    responses = defaultdict(list)
    for line in options_df.iterrows():
        idx = line[1]['file_idx']
        describing_pairs = line[1]['describing_pairs']
        instruction = q_template.format(describing_pairs)
        options = " ".join([line[1]['pair1'],
                            line[1]['pair2'],
                            line[1]['pair3'],
                            line[1]['pair4']])
        response = ask_gpt4(instruction, options)
        responses[idx].append(response)

    return responses


def save_answers(responses, gptans_dir):

    # save the answers
    for idx, subcat_responces in responses.items():
        file_name = f"Phase2Answers-{idx}.txt"
        file_path = os.path.join(gptans_dir, file_name)
        write_answers(subcat_responces, file_path)


@click.command(name="ask_gpt_4")
@click.option('--data_config_path', default='../config/data.yaml')
def get_responses(data_config_path):

    logger.info('Getting GPT-4 answers')
    logger.info('Reading config file')
    config = load_config(data_config_path)
    ph2ans_dir = config['PH2ANS_DIR']
    ph1que_dir = config['PH1QUE_DIR']
    gptque_dir = config['GPTQUE_DIR']
    gptans_dir = config['GPTANS_DIR']
    selected_idxs = config['SELECTED_IDXS']
    q_template = config['Q_TEMPLATE']

    logger.info('Preparing questions')
    options_df = prepare_questions(ph2ans_dir, ph1que_dir,
                                   gptque_dir, selected_idxs)

    logger.info('Asking the questions')
    responses = send_questions(options_df, q_template)

    logger.info('Saving the answers')
    save_answers(responses, gptans_dir)

    logger.info('Answers have been received and saved')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    get_responses()
