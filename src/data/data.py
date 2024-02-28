import re
import pandas as pd
import csv
import yaml


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def read_txt_info(path):
    with open(path, 'r') as f:
        info = f.read()
    return info


def read_hum_answers(path):
    df = pd.read_csv(path, sep='\t')
    df = df.rename({'# pair1': 'pair1'}, axis='columns')
    return df


def read_gpt_answers(path):
    df = pd.read_csv(path, sep=', ',
                     names=['pair1', 'pair2',
                            'pair3', 'pair4',
                            'least_illustrative',
                            'most_illustrative'],
                     engine='python')
    return df


def read_cat_info(path):
    df = pd.read_csv(path, header=None,
                     names=['num', 'letter', 'cat', 'subcat'])
    df['file_idx'] = df['num'].astype(str) + \
        df['letter'].apply(lambda x: x.replace(' ', ''))
    return df


def read_reversals_info(path):
    with open(path, 'r') as f:
        reversals = f.read()

    reversals = reversals.split('original:pair --> reversed:pair')[-1]

    idxs = re.findall('[0-9]+[a-z]', reversals)
    pairs = re.findall('--> [A-Z, a-z]+:[A-Z, a-z]+', reversals)
    pairs = list(map(lambda x: x.split('--> ')[-1], pairs))

    reversal_df = pd.DataFrame({'idxs': idxs, 'pair': pairs})
    return reversal_df


def write_answers(responses, path):
    with open(path, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        for response in responses:
            writer.writerow([response])
