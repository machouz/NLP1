from Estimator import *
from datetime import datetime
import numpy as np

start = datetime.now()

input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"
treshold = 10

print "The treshold is " + str(treshold)

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

def getScore(word, index, tag, prev_tag, prev_prev_tag, emission):
    V = Viterbi[index - 1][prev_tag] + Viterbi[index - 2][prev_prev_tag]
    a = np.log(estimator.getQ(prev_prev_tag, prev_tag, tag))
    b = -np.log(emission)

    return V + a + b


possibles_bigrams = preprocessing()


dic_label = {key: -np.inf for key in estimator.tag_unigram}
dic_label_str = dic_label.copy()
dic_label_str['STR'] = 0


for ind, sentence in enumerate(data[:10]):
    Viterbi = []
    tags = []

    print ind
    Viterbi.append(dic_label_str)
    Viterbi.append(dic_label_str)


    for i in xrange(2, len(sentence)):
        tags_dic = dic_label.copy()
        word_dic = dic_label.copy()
        possibilities_score = []
        word = sentence[i]

        for tag in word_dic:
            emission = estimator.getE(word, tag)
            possibilities_score = []
            if emission > 0.0:
                for prev_prev_tag, prev_tag in possibles_bigrams[tag]:
                    prob = getScore(word, i, tag, prev_tag, prev_prev_tag, emission)
                    possibilities_score.append([prob, prev_tag])

            if len(possibilities_score) != 0:
                score, prev_tag = max(possibilities_score)
                word_dic[tag] = score
                tags_dic[tag] = prev_tag


        Viterbi.append(word_dic)
        tags.append(tags_dic)

    predict_last_tag = max(Viterbi[i].keys(), key=Viterbi[i].get)
    sentence[i] = [sentence[i], predict_last_tag]
    for j in xrange(i-1, 2, -1):
        tag_j = tags[i - 2]
    prev_prev, prev_tag = tags[i - 2][predict_last_tag]


    #for j in range(len(sentence), 2, -1):
    #    predict_tag = max(Viterbi[j - 1].keys(), key=Viterbi[j].get)
    #    tag = predict_tag[1]





good = 0.0
total = 0.0
labels = read_data("../data/ass1-tagger-test")


for i in xrange(len(data[:10])):
    for word_p, word_l in zip(data[i][2:], labels[i][2:]):
        if word_p[1] == word_l[1]:
            good += 1
        total += 1

acc = good / total
print "Accuracy : " + str(acc)

zman = datetime.now() - start
print(zman)

