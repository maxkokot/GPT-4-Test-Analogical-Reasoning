import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import logging
import yaml
import click


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def load_txt(path):
    with open(path, 'r') as f:
        file = f.read()
    return file


def send_request(client, message):
    body = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
                                              model="gpt-3.5-turbo",
                                              messages=body
                                              )
    return response.choices[0].message["content"].strip()


def llm(config_path):

    config = load_config(config_path)
    processed_data_path = config['processed_train_data_path']

    # this loads your open api key from .env file
    _ = load_dotenv(find_dotenv())
    client = OpenAI()
    logger.info('Client has been started')

    lst_questionnaries = os.listdir(processed_data_path)

    for q in lst_questionnaries:
        prompt = load_txt(os.path.join(processed_data_path, q))
        logger.info('Sending request...')
        send_request(client, prompt)

    # TODO: buy access to API and save results


@click.command(name="gpt")
@click.option('--data_config_path', default='../../config/data.yaml')
def connect(data_config_path):
    logger.info('Getting GPT-4 answers')
    llm(data_config_path)
    logger.info('Answers have been received and saved')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    connect()
