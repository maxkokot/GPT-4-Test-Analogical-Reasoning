import os
import re
import pandas as pd
import logging
import click

from data.data import load_config, read_cat_info, \
    read_hum_answers, read_gpt_answers, write_answers
from evaluation.maxdiff import maxdiff, pairqnum2least, \
    pairqnum2most, calc_maxdiff_acc
from evaluation.spearman import calc_spearman


def read_all_answers(ph2ans_dir, gptans_dir):
    lst_files = os.listdir(gptans_dir)
    lst_hum_dfs = []
    lst_gpt_dfs = []

    for file_name in lst_files:

        idx = re.findall('[0-9]+[a-z]', file_name)[0]
        ans_name = f"Phase2Answers-{idx}.txt"

        # reading answers provived by humans
        # on the questions related to
        # current subcategory
        ans_path = os.path.join(ph2ans_dir, ans_name)
        hum_df = read_hum_answers(ans_path)
        hum_df['file_idx'] = idx
        lst_hum_dfs.append(hum_df)

        # reading answers provived by GPT
        # on the questions related to
        # current subcategory
        gpt_ans_path = os.path.join(gptans_dir, ans_name)
        gpt_df = read_gpt_answers(gpt_ans_path)
        # add name of user selected relation
        rel_name = hum_df['user_selected_relation'].unique()[0]
        gpt_df['user_selected_relation'] = rel_name
        gpt_df['file_idx'] = idx
        lst_gpt_dfs.append(gpt_df)

    hum_data = pd.concat(lst_hum_dfs).reset_index(drop=True)
    gpt_data = pd.concat(lst_gpt_dfs).reset_index(drop=True)

    return hum_data, gpt_data


def evaluate_maxdiff(hum_data, gpt_data):

    # for each question and each pair compute
    # how many times the pair was selected as least and most
    # illustrative example for the question
    # according to human answers

    least_data = hum_data.groupby(['pair1', 'pair2',
                                   'pair3', 'pair4']).\
                                    apply(lambda x: pairqnum2least(x))
    most_data = hum_data.groupby(['pair1', 'pair2',
                                  'pair3', 'pair4']).\
                                   apply(lambda x: pairqnum2most(x))

    maxdiff_data = gpt_data.apply(lambda x: maxdiff(x, least_data,
                                                    most_data),
                                  axis=1)

    # calculate maxdiff accuracy

    # first calculate it across all subcatigories
    maxdiff_acc_subcat = maxdiff_data.groupby('user_selected_relation')\
        .apply(lambda x: calc_maxdiff_acc(x))
    # then average them
    maxdiff_acc_avg = maxdiff_acc_subcat.mean()
    maxdiff_acc_avg

    return maxdiff_acc_avg


def evaluate_spearman(hum_data, gpt_data):

    spearman_df = gpt_data.groupby('user_selected_relation').\
        apply(lambda x: calc_spearman(x, hum_data))
    spearman_coef = spearman_df.rho.mean()
    return spearman_coef


@click.command(name="ask_gpt_4")
@click.option('--data_config_path', default='../config/data.yaml')
def evaluate(data_config_path):

    logger.info('Evaluating GPT-4 answers')
    logger.info('Reading config file')
    config = load_config(data_config_path)
    ph2ans_dir = config['PH2ANS_DIR']
    gptans_dir = config['GPTANS_DIR']

    logger.info('Reading GPT-4 and human answers')
    hum_data, gpt_data = read_all_answers(ph2ans_dir,
                                          gptans_dir)

    logger.info('Evaluating MaxDiff Accuracy')
    maxdiff_acc_avg = evaluate_maxdiff(hum_data, gpt_data)
    logger.info(f'MaxDiff Accuracy = {round(maxdiff_acc_avg, 2)}')

    logger.info('Evaluating Spearman Rank Correllation Coefficient')
    spearman_coef = evaluate_spearman(hum_data, gpt_data)
    logger.info(f"Spearman Rank Correllation \
Coefficient = {round(spearman_coef, 2)}")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    evaluate()
