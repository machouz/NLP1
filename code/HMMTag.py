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



sentence = data[0]
for i in xrange(len(sentence)):



#def getScore(word, tag, prev_tag, prev_prev_tag):
