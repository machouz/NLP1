from Estimator import *
from datetime import datetime
import numpy as np
from sys import argv

start = datetime.now()

input_file = argv[1]
q_file = argv[2]
e_file = argv[3]

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
    V = Viterbi[index - 1][prev_tag] + Viterbi[index - 2][prev_prev_tag]
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

dic_label = {key: -np.inf for key in estimator.tag_unigram}
dic_label_str = dic_label.copy()
dic_label_str['STR'] = 0

print datetime.now() - start

for ind, sentence in enumerate(data[:10]):
    Viterbi = [dic_label_str, dic_label_str]
    tags = []

    print ind

    for i in xrange(2, len(sentence)):
        tags_dic = dic_label.copy()
        word_dic = dic_label.copy()
        word = sentence[i]

        for tag in word_dic:
            emission = estimator.getE(word, tag)
            if emission > 0.0:
                possibilities_score = []
                for prev_prev_tag, prev_tag in possibles_bigrams:  # [tag]:
                    prob = getScore(word, i, tag, prev_tag, prev_prev_tag, emission)
                    possibilities_score.append([prob, prev_tag])

                score, prev_tag = max(possibilities_score)
                word_dic[tag] = score
                tags_dic[tag] = prev_tag

        Viterbi.append(word_dic)
        tags.append(tags_dic)

    prev_tag = max(Viterbi[-1].keys(), key=Viterbi[-1].get)
    sentence[-1] = [sentence[-1], prev_tag]
    for j in range(len(sentence) - 2, 1, -1):
        j_tag = tags[j - 1][prev_tag]
        sentence[j] = [sentence[j], j_tag]
        prev_tag = j_tag

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
