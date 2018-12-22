import multiprocessing
from datetime import datetime
from sys import argv
import numpy as np
import pickle
import sys
import os
# from ass1.Estimator import *
from utils import *

# ../data/ass1-tagger-test-input ./memm1/model ./memm1/feature_map test_output
start = datetime.now()

input_file = argv[1]
model_file = argv[2]
feature_map_file = argv[3]
out_file_name = argv[4]

model = pickle.load(open(model_file, 'rb'))

print(datetime.now() - start)

features2id = file_to_dic(feature_map_file)
id2features = {v: k for k, v in features2id.iteritems()}
zero_features_vector = np.zeros(max(features2id.values()))


def feature_convert(features_dic):
    features_vec = zero_features_vector.copy()
    for key, value in features_dic.items():
        if str(key) + "=" + str(value) in features2id:
            feature = features2id[key + "=" + value]
            features_vec[feature - 1] = 1
    return features_vec


def get_features(index, line):
    features = {}
    current_word = line[index]
    features["current_word"] = current_word

    if index > 0:
        previous_word, previous_tag = line[index - 1]
        # features["previous_word"] = previous_word
        features["previous_tag"] = previous_tag

    '''
    if index > 1:
        pre_previous_word, pre_previous_tag = line[index - 2]
        features["pre_previous_tag"] = pre_previous_tag
        # features["pre_previous_word"] = pre_previous_word

    '''

    if len(line) > index + 1:
        next_word = line[index + 1][0]
        # features["next_word"] = next_word

    if len(line) > index + 2:
        next_next_word = line[index + 2][0]
        # features["next_next_word"] = next_next_word

    return features


data = []

for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split(" ")
    data.append(arr)


def func(sentence):
    i, sentence = sentence
    print i
    for i in range(2, len(sentence)):
        features_dic = get_features(i, sentence)
        features_vec = feature_convert(features_dic)
        tag_index = model.predict([features_vec])
        current_tag = id2features[tag_index[0]]
        sentence[i] = [sentence[i], current_tag]
    return sentence


pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
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

write_to_file(out_file_name, output)

print(datetime.now() - start)

print "Greedy MEMM"
