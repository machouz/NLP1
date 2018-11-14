import MLETrain
from utils import *


input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"

data = []
for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)

'''
q_mle = file_to_dic(q_file)

Q_trigram = {}
Q_bigram = {}
Q_unigram = {}

for key, value in q_mle.items():
    gram = key.split()
    if len(gram) == 3:
        Q_trigram[key] = int(value)
    elif len(gram) == 2:
        Q_bigram[key] = int(value)
    else:
        Q_unigram[key] = int(value)


E_probs = file_to_dic(e_file)

'''


for sentence in data:
    for i in range(2, len(sentence)):
        a, b, c = sentence[i-2], sentence[i-1], sentence[i]
        t1, t2 = a[1], b[1]
        probs = {x : MLETrain.getQ(t1, t2, x) * MLETrain.getE(c, x) for x in MLETrain.Q_unigram}
        t3 = max(probs, key=probs.get)
        sentence[i] = [sentence[i], t3]




good = 0.0
labels = read_data("../data/ass1-tagger-test")

for i in xrange(len(data)):
    for word_p, word_l in zip(data[i], labels[i]):
        if word_p[1] == word_l[1]:
            good += 1

words_num = sum(len(x) for x in data)
acc = good / words_num
print "Accuracy : " + str(acc)

