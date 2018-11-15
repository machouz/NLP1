from Estimator import *
from datetime import datetime

start = datetime.now()

input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"

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
        for key in estimator.tag_trigram:
            trigram = key.split()
            if tag == trigram[-1]:
                possible_bigrams.append(trigram[:-1])
        dic[tag] = possible_bigrams
    return dic

def getScore(word, index, tag, prev_tag, prev_prev_tag):
    V = Viterbi[index - 1][prev_tag] * Viterbi[index - 2][prev_prev_tag]
    a = estimator.getQ(prev_prev_tag, prev_tag, tag)
    b = estimator.getE(word, tag)

    return  V * a * b


possibles_bigrams = preprocessing()

Viterbi = []

dic_label = {key: 0 for key in estimator.tag_unigram}
dic_label_str = dic_label.copy()
dic_label_str['STR'] = 1



for sentence in data:
    #sentence = data[0]
    Viterbi.append(dic_label_str)
    Viterbi.append(dic_label_str)


    
    for i in xrange(2, len(sentence)):
        word_dic = dic_label.copy()
        possibilities_score = []

        for tag in word_dic:
            for prev_prev_tag, prev_tag in possibles_bigrams[tag]:
                possibilities_score.append(getScore(sentence[i], i, tag, prev_tag, prev_prev_tag))

            word_dic[tag] = max(possibilities_score)

        tag_predict = max(word_dic, key=word_dic.get)
        sentence[i] = [sentence[i], tag_predict]

        Viterbi.append(word_dic)


