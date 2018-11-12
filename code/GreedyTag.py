import MLETrain
from utils import *


input_file = "../data/ass1-tagger-test-input"
q_file = "q.mle"
e_file = "e.mle"

data = []
for line in file(input_file):
    arr = [['***', 'STR'], ['***', 'STR']] + line[:-1].split()
    data.append(arr)


q_mle = file_to_dic(q_file)
e_mle = file_to_dic(e_file)

for sentence in data:
    for i in range(2, len(sentence)):
        a, b, c = sentence[i-2], sentence[i-1], sentence[i]
        t1, t2 = a[1], b[1]
        probs = {x : MLETrain.getQ(t1, t2, x) * MLETrain.getE(c, x) for x in MLETrain.Q_unigram}
        t3 = max(probs, key=probs.get)
        sentence[i] = [sentence[i], t3]

