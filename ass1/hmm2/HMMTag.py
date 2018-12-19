from datetime import datetime
import numpy as np
import copy
from sys import argv
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from ass1.Estimator import *

start = datetime.now()

input_file = argv[1]
q_file = argv[2]
e_file = argv[3]
output_file = argv[4]


data = []
estimator = Estimator()
estimator.load_from_file(q_file, e_file)


for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)


def prep():
    return [[tag1, tag2] for tag1 in estimator.tag_unigram for tag2 in estimator.tag_unigram]


def find_possible_previous_tag():
    possible_tags = {}
    for tag in estimator.tag_unigram:
        possible_tags[tag] = []
    for bigram, number in estimator.tag_bigram.items():
        label1, label2 = bigram.split(' ')
        possible_tags[label2].append(label1)

    return possible_tags

def getScore(word, index, tag, prev_tag, prev_prev_tag, emission=None):
    V = Viterbi[index - 1][prev_prev_tag][prev_tag]
    a = np.log(estimator.getQ(prev_prev_tag, prev_tag, tag))
    if emission is not None:
        b = np.log(emission)
    else:
        emission = estimator.getE(word, tag)
        if emission == 0:
            b = -np.inf
        else:
            b = np.log(emission)

    return V + a + b


possibles_bigrams = prep()  # rocessing()

dic_label = {key1: {key2: -np.inf for key2 in estimator.tag_unigram} for key1 in estimator.tag_unigram}

dic_label_str = copy.deepcopy(dic_label)
dic_label_str['STR']['STR'] = 0


possible_previous_tag = find_possible_previous_tag()

print datetime.now() - start


for ind, sentence in enumerate(data):
    Viterbi = [copy.deepcopy(dic_label_str), copy.deepcopy(dic_label_str)]

    tags = []

    print ind

    for i in xrange(2, len(sentence)):
        tags_dic = copy.deepcopy(dic_label)
        word_dic = copy.deepcopy(dic_label)
        word = sentence[i]

        for r in estimator.tag_unigram: #current
            emission = estimator.getE(word, r)
            if emission > 0.0:
                for t in possible_previous_tag[r]: #prev
                    possibilities_score = []

                    for t_tag in possible_previous_tag[t]:  # prev_prev
                        prob = getScore(word, i, r, t, t_tag, emission)
                        possibilities_score.append([prob, t_tag])

                    score, prev_prev = max(possibilities_score)
                    word_dic[t][r] = score
                    tags_dic[t][r] = prev_prev



        Viterbi.append(word_dic)
        tags.append(tags_dic)

    prev_prev, prev = max_nested_dic(Viterbi[i])

    sentence[-1] = [sentence[-1], prev]
    sentence[-2] = [sentence[-2], prev_prev]


    for j in range(len(sentence) - 3, 1, -1):
        j_tag = tags[j][prev_prev][prev]
        sentence[j] = [sentence[j], j_tag]
        prev = prev_prev
        prev_prev = j_tag



output = []
for line in data:
    str = ''
    for word, tag in line[2:]:
        str += word + '/' + tag + ' '
    output.append(str[:-1])

write_to_file(output_file, output)

print "Viterbi hmm"

zman = datetime.now() - start
print(zman)
