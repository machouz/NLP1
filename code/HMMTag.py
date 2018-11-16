from Estimator import *
from datetime import datetime
import numpy as np

start = datetime.now()

input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"
treshold = 5

data = []
estimator = Estimator()
estimator.load_from_file(q_file, e_file)

load_time = datetime.now() - start
print(load_time)

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

def getScore(word, index, tag, prev_tag, prev_prev_tag):
    V = Viterbi[index - 1][prev_tag] + Viterbi[index - 2][prev_prev_tag]
    a = np.log(estimator.getQ(prev_prev_tag, prev_tag, tag))
    b = np.log(estimator.getE(word, tag))

    return  V + a + b


possibles_bigrams = preprocessing()

Viterbi = []

dic_label = {key: -np.inf for key in estimator.tag_unigram}
dic_label_str = dic_label.copy()
dic_label_str['STR'] = 0


for sentence in data[:1]:
    Viterbi.append(dic_label_str)
    Viterbi.append(dic_label_str)


    for i in xrange(2, len(sentence)):
        word_dic = dic_label.copy()
        #possibilities_score = []

        for tag in word_dic:
            possibilities_score = []
            for prev_prev_tag, prev_tag in possibles_bigrams[tag]:
                possibilities_score.append(getScore(sentence[i], i, tag, prev_tag, prev_prev_tag))

            if len(possibilities_score) != 0:
                word_dic[tag] = max(possibilities_score)

        tag_predict = max(word_dic, key=word_dic.get)
        sentence[i] = [sentence[i], tag_predict]

        Viterbi.append(word_dic)


'''
good = 0.0
labels = read_data("../data/ass1-tagger-test")


for i in xrange(len(data)):
    for word_p, word_l in zip(data[i][2:], labels[i][2:]):
        if word_p[1] == word_l[1]:
            good += 1

words_num = sum(len(x) - 2 for x in data)
acc = good / words_num
print "Accuracy : " + str(acc)

zman = datetime.now() - start
print(zman)
'''
