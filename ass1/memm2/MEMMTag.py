from datetime import datetime
from sys import argv
import numpy as np
import pickle
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from ass1.utils import *


# ../data/ass1-tagger-test-input ./memm1/model ./memm1/feature_map
start = datetime.now()
input_file = argv[1]
model_file = argv[2]
feature_map_file = argv[3]
#out_file_name = argv[4]

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


def get_features(current_word, pre_previous_tag, pre_previous_word, previous_tag, previous_word, next_word=None,
                 next_next_word=None):
    features = {}
    features["current_word"] = current_word

    features["previous_word"] = previous_word
    features["previous_tag"] = previous_tag
    if pre_previous_tag:
        features["pre_previous_tag"] = pre_previous_tag

    features["pre_previous_word"] = pre_previous_word

    if next_word:
        features["next_word"] = next_word

    if next_next_word:
        features["next_next_word"] = next_next_word

    return features


def getScore(index, tag, vec_pred):
    if index == 2:
        V = 1
    elif index == 3:
        V = Viterbi[index - 1]
    else:
        V = Viterbi[index - 1] * Viterbi[index - 2]
    score = vec_pred[tag]
    return V * score


data = []
for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)

print datetime.now() - start

for ind, sentence in enumerate(data):
    Viterbi = []

    tags = []

    scores = []

    for i in xrange(2, len(sentence)):
        current_word = sentence[i]
        prev_tags_score = np.zeros(46)
        prev_tags = np.zeros(46)

        for prev_tag in xrange(0, 46):
            features_dic = get_features(current_word=current_word,
                                        pre_previous_tag=None if i > 3 else "STR",
                                        pre_previous_word=sentence[i - 2] if i > 3 else "***",
                                        previous_tag=prev_tag if i > 2 else "STR",
                                        previous_word=sentence[i - 2] if i > 2 else "***",
                                        next_word=sentence[i + 1] if len(sentence) > i + 1 else None,
                                        next_next_word=sentence[i + 2] if len(sentence) > i + 2 else None)
            features_vec = feature_convert(features_dic)
            vec_pred = model.predict_proba([features_vec])
            tag = vec_pred.argmax(axis=1)[0]
            score, prev = vec_pred[0][tag], tag
            prev_tags[prev_tag] = score
            prev_tags_score[prev_tag] = prev

        Viterbi.append(prev_tags_score)
        tags.append(prev_tags)

    last = tags[-1][Viterbi[-1].argmax(axis=0)]

    sentence[-1] = [sentence[-1], last]

    for j in range(len(sentence) - 3, 1, -1):
        j_tag = tags[j][last]
        sentence[j] = [sentence[j], j_tag]
        last = j_tag

output = []
for line in data:
    str = ''
    for word, tag in line[2:]:
        str += word + '/' + tag + ' '
    output.append(str[:-1])

write_to_file(out_file_name, output)

print "Viterbi hmm"

zman = datetime.now() - start
print(zman)
