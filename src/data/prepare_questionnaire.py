import os
import re
import random
import click
import yaml
import logging


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def load_txt(path):
    with open(path, 'r') as f:
        file = f.read()
    return file


def write_questionarie(questionnaire, proccesed_dir, idx):
    with open(os.path.join(proccesed_dir,
              f'Questionnaire-{idx}.txt'), 'w') as f:
        f.write(questionnaire)


def get_questions_dir_path(start_pth, phase):

    contains = os.listdir(start_pth)
    phase_dir = list(filter(lambda x: phase in x, contains))
    phase_questions_dir = list(filter(lambda x: 'Questions' in x, phase_dir))
    phase_questions_dir_path = os.path.join(start_pth, phase_questions_dir[0])
    return phase_questions_dir_path


def read_questions(phase_questions_dir_path):
    questions = {}
    phase_questions_files = os.listdir(phase_questions_dir_path)
    for file_name in phase_questions_files:
        idx = re.findall('[0-9]+[a-z]', file_name)[0]
        file_path = os.path.join(phase_questions_dir_path, file_name)
        question = load_txt(file_path)
        questions[idx] = question
    return questions


def prepare_ph1_question_1(raw_file, template):

    # remove correct answer
    prepared_question = re.sub('\n*Correct Answer(.|\n)*', '', raw_file)

    # remove topic
    prepared_question = re.sub('Question.*\n*', '', prepared_question)
    prepared_question = f'Question 1: {prepared_question}'

    # add (a), (b), (c) and so forth
    intro, options = prepared_question.split('?\n\n')
    options = options.split('\n')
    options = [f'({i + 1}) {options[i]}' for i in range(len(options))]

    prepared_question = intro + '?\n\n' + '\n'.join(options) + '\n\n'
    return prepared_question


def prepare_ph1_question_2(raw_file, template):

    # extract pairs
    pairs = re.findall('[a-z]+:[a-z]+', raw_file)
    pairs = '\n'.join(pairs)

    prepared_question = template.format(pairs)
    return prepared_question


def prepare_ph2_question_1(raw_file, template):

    # same as 1st phase
    return prepare_ph1_question_1(raw_file,
                                  template)


def prepare_ph2_question_2(raw_file_1,
                           raw_file_2,
                           template):

    # extract pairs
    query_pairs = re.findall('[a-z]+:[a-z]+', raw_file_1)
    query_pairs = ', '.join(query_pairs)

    # randomly select 4 possible answers
    answers_list = raw_file_2.split('\n')
    responce_pairs = random.choice(answers_list)
    responce_pairs = responce_pairs.split(',')
    responce_pairs = [f'({i + 1}) {responce_pairs[i]}'
                      for i in range(len(responce_pairs))]
    responce_pairs = '\n'.join(responce_pairs)

    prepared_question = template.format(query_pairs, responce_pairs)
    return prepared_question


def merge_questions(processed_pth,
                    ph1_intro_template,
                    ph2_intro_template,
                    ph1_questions,
                    ph2_questions,
                    ph1_q1_template,
                    ph1_q2_template,
                    ph2_q1_template,
                    ph2_q2_template):

    for idx in ph1_questions.keys():
        ph1q1 = prepare_ph1_question_1(ph1_questions[idx],
                                       ph1_q1_template)
        ph1q2 = prepare_ph1_question_2(ph1_questions[idx],
                                       ph1_q2_template)
        ph2q1 = prepare_ph2_question_1(ph1_questions[idx],
                                       ph2_q1_template)
        ph2q2 = prepare_ph2_question_2(ph1_questions[idx],
                                       ph2_questions[idx],
                                       ph2_q2_template)
        questionnaire = f"{ph1_intro_template}{ph1q1}{ph1q2}"\
                        f"{ph2_intro_template}{ph2q1}{ph2q2}"

        write_questionarie(questionnaire, processed_pth, idx)


def make(config_path):

    config = load_config(config_path)

    raw_data_path = config['raw_train_data_path']
    processed_data_path = config['processed_train_data_path']
    ph1_intro_template = config['ph1_intro_template']
    ph2_intro_template = config['ph2_intro_template']
    ph1_q1_template = config['ph1_q1_template']
    ph1_q2_template = config['ph1_q2_template']
    ph2_q1_template = config['ph2_q1_template']
    ph2_q2_template = config['ph2_q2_template']

    logger.info(f'Raw data path: {raw_data_path}')

    ph1_questions_path = get_questions_dir_path(raw_data_path, 'Phase1')
    ph2_questions_path = get_questions_dir_path(raw_data_path, 'Phase2')

    ph1_questions = read_questions(ph1_questions_path)
    ph2_questions = read_questions(ph2_questions_path)

    merge_questions(processed_data_path,
                    ph1_intro_template,
                    ph2_intro_template,
                    ph1_questions,
                    ph2_questions,
                    ph1_q1_template,
                    ph1_q2_template,
                    ph2_q1_template,
                    ph2_q2_template)

    logger.info(f'Questionnaires have been saved in: {processed_data_path}')


@click.command(name="questionnaire")
@click.option('--data_config_path', default='../../config/data.yaml')
def make_questionnaire(data_config_path):
    logger.info('Making Questionnaire')
    make(data_config_path)
    logger.info('Questionnaires have been created and saved')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    make_questionnaire()
