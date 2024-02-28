import numpy as np


def pairqnum2least(question_data):
    df = question_data['least_illustrative'].value_counts()
    return df


def pairqnum2most(question_data):
    return question_data['most_illustrative'].value_counts()


def extract_voices(pairs, pair,
                   ref_data):

    multiidx = tuple(np.append(pairs, pair))

    if multiidx in ref_data.index:
        votes = ref_data.loc[multiidx]
    else:
        votes = 0

    return votes


def maxdiff(answer, least_data, most_data):

    least_ans = answer['least_illustrative']
    most_ans = answer['most_illustrative']
    pairs = answer[['pair1', 'pair2', 'pair3', 'pair4']].values.ravel()

    votes_guess_least = extract_voices(pairs, least_ans,
                                       least_data)
    votes_guess_most = extract_voices(pairs, most_ans, most_data)

    num_votes_least = []
    num_votes_most = []

    for pair in pairs:

        num_votes_least.append(extract_voices(pairs, pair, least_data))
        num_votes_most.append(extract_voices(pairs, pair, most_data))

    max_votes_least = max(num_votes_least)
    max_votes_most = max(num_votes_most)

    maxdiff_df = answer.copy()
    maxdiff_df['num_least_right'] = int(votes_guess_least == max_votes_least)
    maxdiff_df['num_least_wrong'] = int(votes_guess_least != max_votes_least)
    maxdiff_df['num_most_right'] = int(votes_guess_most == max_votes_most)
    maxdiff_df['num_most_wrong'] = int(votes_guess_most != max_votes_most)

    return maxdiff_df


def calc_maxdiff_acc(rel_data):
    acc_all = 100 * (rel_data.num_most_right.sum() +
                     rel_data.num_least_right.sum()) \
                        / (2 * len(rel_data))
    return acc_all
