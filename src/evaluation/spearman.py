import pandas as pd
import numpy as np
from scipy.stats import spearmanr


def calc_rating_scores(questions):

    '''
    calculates golden standard ratings
    '''

    raveled_pairs = questions[['pair1', 'pair2',
                               'pair3', 'pair4']].values.ravel()
    all_pairs = np.unique(raveled_pairs)
    rating_scores = {}

    for pair in all_pairs:
        rating_scores[pair] = calc_one_rating(pair, raveled_pairs,
                                              questions)

    return rating_scores


def calc_one_rating(pair, raveled_pairs, questions):

    pair_num_least = (questions.least_illustrative == pair).sum()
    pair_num_most = (questions.most_illustrative == pair).sum()
    pair_num = (raveled_pairs == pair).sum()
    pct_least = 100 * pair_num_least / pair_num
    pct_most = 100 * pair_num_most / pair_num
    score = pct_most - pct_least
    return score


def calc_spearman(gpt_data_subcat, hum_data):
    name_subcat = gpt_data_subcat.user_selected_relation.unique()[0]
    hum_data_subcat = hum_data[hum_data['user_selected_relation'] ==
                               name_subcat]
    pair2gold = calc_rating_scores(hum_data_subcat)
    pair2test = calc_rating_scores(gpt_data_subcat)

    cor = spearmanr(list(pair2gold.values()),
                    list(pair2test.values()))
    rho = cor.correlation
    pvalue = cor.pvalue

    return pd.DataFrame([{'rho': rho, 'pvalue': pvalue}])


def find_reversals(question):

    global reversal_df

    question['with_reversals'] = 0
    rel_name = question['user_selected_relation']
    pairs = question[['pair1', 'pair2', 'pair3', 'pair4']]
    reversals = reversal_df[reversal_df.user_selected_relation ==
                            rel_name].pair

    if reversals.isin(pairs).sum():
        question['with_reversals'] = 1

    return question


def remove_reversals(data):
    data_no_rev = data.apply(lambda x: find_reversals(x), axis=1)
    data_no_rev = data_no_rev[data_no_rev['with_reversals'] == 0].\
        reset_index(drop=True)
    data_no_rev.drop('with_reversals', axis=1, inplace=True)
    return data_no_rev
