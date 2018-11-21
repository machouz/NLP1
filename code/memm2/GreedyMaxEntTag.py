from datetime import datetime
from code.memm1.ExtractFeatures import get_features
from sys import argv
from code.utils import *
import numpy as np
import pickle

start = datetime.now()
input_file = argv[1]
model_file = argv[2]
feature_map_file = argv[3]
# out_file_name = argv[4]

model = pickle.load(open(model_file, 'rb'))

print(datetime.now() - start)

features2id = file_to_dic(feature_map_file)
id2features = {v: k for k, v in features2id.iteritems()}
zero_features_vector = np.zeros(max(features2id.values()) + 1)


def feature_convert(features_dic):
    features_vec = zero_features_vector.copy()
    for key, value in features_dic.items():
        if str(key) + "=" + str(value) in features2id:
            feature = features2id[key + "=" + value]
            features_vec[feature] = 1

    return features_vec


data = []

for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)
for sentence in data[:10]:
    for i in range(2, len(sentence)):
        features_dic = get_features(i, sentence)
        features_vec = feature_convert(features_dic)
        print features_vec
        tag_index = model.predict([features_vec])
        current_tag = id2features[tag_index[0]]
        sentence[i] = [sentence[i], current_tag]

good = 0.0
total = 0.0
labels = read_data("../data/ass1-tagger-test")

error = []

for i in xrange(len(data[:10])):
    for word_p, word_l in zip(data[i][2:], labels[i][2:]):
        if word_p[1] == word_l[1]:
            good += 1
        else:
            error.append([i, word_l[0], word_l[1], word_p[1]])
        total += 1

acc = good / total
print "Accuracy : " + str(acc)

zman = datetime.now() - start
print(zman)

"""
runfile('/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code/ExtractFeatures.py', args='../data/ass1-tagger-train features', wdir='/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code')
runfile('/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code/ConvertFeatures.py', args='features feature_vecs feature_map', wdir='/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code')
runfile('/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code/TrainSolver.py', args='feature_vecs model', wdir='/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code')
runfile('/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code/GreedyMaxEntTag.py', args='../data/ass1-tagger-test-input model feature_map', wdir='/Users/machou/Documents/Machon Lev/Chana 5/Semestre 1/NLP/Ass1/code')
"""
