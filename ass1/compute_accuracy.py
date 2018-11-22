import sys
from utils import *

pred = sys.argv[1]
label = sys.argv[2]

good = 0.0
total = 0.0

#pred = 'hmm2/greedy_output'
#label = '../data/ass1-tagger-test'

label_acc = {}

pred = read_data(pred)
label = read_data(label)
for i in xrange(len(pred)):
    for w1, w2 in zip(pred[i][2:], label[i][2:]):
        lab = w2[1][-4:] if len(w2[1]) >= 3 else w2[1]
        if lab not in label_acc:
            label_acc[lab] = [0, 0]

        totalL = label_acc[lab][1] + 1
        goodL = label_acc[lab][0]
        if w1[1] == w2[1]:
            good += 1
            label_acc[lab] = [goodL + 1, totalL]
        total += 1

        label_acc[lab][1] = totalL

acc = good / total

print "Accuracy " + str(acc)

for tag, dic in label_acc.items():
    ac = float(dic[0]) / float(dic[1])
    print tag, ac