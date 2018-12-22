import copy
import multiprocessing
from datetime import datetime
from sys import argv
import numpy as np
import pickle
import os
import sys
from utils import *

# ../data/ass1-tagger-test-input ./memm1/model ./memm1/feature_map
start = datetime.now()
input_file = argv[1]
model_file = argv[2]
feature_map_file = argv[3]
output_file = argv[4]
data = []

for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split(" ")
    data.append(arr)

model = pickle.load(open(model_file, 'rb'))

print(datetime.now() - start)

features2id = file_to_dic(feature_map_file)
id2features = {v: k for k, v in features2id.iteritems()}
zero_features_vector = np.zeros(max(features2id.values()))

possible_tags = ["PRP$", "VBG", "VBD", "``", "VBN", "POS", "''", "VBP", "WDT", "JJ", "WP", "VBZ", "DT", "#",
                 "RP", "$",
                 "NN", ")", "(", "FW", ",", ".", "TO", "PRP", "RB", ":", "NNS", "NNP", "VB", "WRB", "CC", "LS", "PDT",
                 "RBS", "RBR", "CD", "EX", "IN", "WP$", "MD", "NNPS", "JJS", "JJR", "UH", ]
possible_prev_tags = ["STR"] + possible_tags
posible_tags_id = map(lambda x: (x, np.array([features2id[x]], dtype='float64')), possible_tags)


def feature_convert(features_dic):
    features_vec = zero_features_vector.copy()
    for key, value in features_dic.items():
        if str(key) + "=" + str(value) in features2id:
            feature = features2id[key + "=" + value]
            features_vec[feature - 1] = 1
    return features_vec


def get_features(index, line, prev_tag=None):
    features = {}
    current_word = line[index]
    features["current_word"] = current_word

    if index > 0:
        if prev_tag:
            features["previous_tag"] = prev_tag
        else:
            previous_word, previous_tag = line[index - 1]
            # features["previous_word"] = previous_word
            features["previous_tag"] = previous_tag

    if index > 1:
        pre_previous_word, pre_previous_tag = line[index - 2]
        features["pre_previous_tag"] = pre_previous_tag

    if len(line) > index + 1:
        next_word = line[index + 1][0]
        # features["next_word"] = next_word

    if len(line) > index + 2:
        next_next_word = line[index + 2][0]
        # features["next_next_word"] = next_next_word

    return features


dic_label_str = {key2: 0 for key2 in possible_prev_tags}
dic_label_str['STR'] = 1.0


def funct(sentence):
    i, sentence = sentence
    print i
    Viterbi = [copy.deepcopy(dic_label_str)]
    bac_prop = ["", ]
    for i in xrange(1, len(sentence)):
        Viterbi.append({})
        bac_prop.append({})
        for tag, arr_tag in posible_tags_id:  # current
            prev_tag = {}
            for prev, value in Viterbi[i - 1].items():  # prev
                features_dic = get_features(i, sentence, prev)
                features_vec = feature_convert(features_dic)
                scr = model.score([features_vec], arr_tag)
                tag_value = value * scr
                prev_tag[prev] = tag_value
            t = max(prev_tag, key=prev_tag.get)
            Viterbi[i][tag] = prev_tag[t]
            bac_prop[i][tag] = t

    last_tag = max(Viterbi[-1], key=Viterbi[-1].get)
    for i in range(len(Viterbi) - 1, 1, -1):
        sentence[i] = [sentence[i], last_tag]
        back_tag = bac_prop[i][last_tag]
        last_tag = back_tag

    return sentence


def func(sentence):
    i, sentence = sentence
    print i
    for i in range(2, len(sentence)):
        features_dic = get_features(i, sentence)
        features_vec = feature_convert(features_dic)
        tag_index = model.predict([features_vec])
        tag_index = model.predict([features_vec])
        tag_index = model.predict([features_vec])
        current_tag = id2features[tag_index[0]]
        sentence[i] = [sentence[i], current_tag]
    return sentence


pool = multiprocessing.Pool(processes=1)
multiple_results = list(pool.map(func, enumerate(data)))
pool.close()
pool.join()

data = multiple_results
output = []
for line in data:
    str = ''
    for word, tag in line[2:]:
        str += word + '/' + tag + ' '
    output.append(str[:-1])

write_to_file(output_file, output)

print "Viterbi MEMM"

zman = datetime.now() - start
print(zman)
