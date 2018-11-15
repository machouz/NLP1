from Estimator import *
from datetime import datetime

start = datetime.now()

input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"
from datetime import datetime

start = datetime.now()
data = []
estimator = Estimator()
estimator.load_from_file(q_file, e_file)

load_time = datetime.now() - start
print(load_time)

for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)

for sentence in data:
    for i in range(2, len(sentence)):
        a, b, c = sentence[i - 2], sentence[i - 1], sentence[i]
        t3 = estimator.get_best_tag(a, b, c)
        sentence[i] = [sentence[i], t3]

good = 0.0
labels = read_data("../data/ass1-tagger-test")



for i in xrange(len(data)):
    for word_p, word_l in zip(data[i][2:], labels[i][2:]):
        if word_p[1] == word_l[1]:
            good += 1

words_num = sum(len(x) for x in data)
acc = good / words_num
print "Accuracy : " + str(acc)


zman = datetime.now() - start
print(zman)
