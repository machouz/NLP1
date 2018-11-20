from Estimator import *
from datetime import datetime
import numpy as np
import copy
from sys import argv

start = datetime.now()

#input_file = argv[1]
#q_file = argv[2]
#e_file = argv[3]

input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"
treshold = 1

print "The treshold is " + str(treshold)

data = []
estimator = Estimator()
estimator.load_from_file(q_file, e_file)


for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)


def preprocessing():
    dic = {}
    for tag in estimator.tag_unigram:
        possible_bigrams = []
        for key, value in estimator.tag_trigram.items():
            trigram = key.split()
            if tag == trigram[-1] and value >= treshold:
                possible_bigrams.append(trigram[:-1])
        dic[tag] = possible_bigrams
    return dic


def prep():
    return [[tag1, tag2] for tag1 in estimator.tag_unigram for tag2 in estimator.tag_unigram]


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
                for t in estimator.tag_unigram: #prev
                    possibilities_score = []

                    for t_tag in estimator.tag_unigram:  # prev_prev
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


good = 0.0
total = 0.0
labels = read_data("../data/ass1-tagger-test")
error = []

for i in xrange(len(data)):
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
