from Estimator import *
from datetime import datetime
from sys import argv

start = datetime.now()

input_file = argv[1]
q_file = argv[2]
e_file = argv[3]

data = []
estimator = Estimator()
estimator.load_from_file(q_file, e_file)

for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)

for sentence in data:
    for i in range(2, len(sentence)):
        a, b, c = sentence[i - 2], sentence[i - 1], sentence[i]
        t3 = estimator.get_best_tag(a, b, c)
        sentence[i] = [sentence[i], t3]

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