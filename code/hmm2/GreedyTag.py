from code.Estimator import *
from datetime import datetime
from sys import argv

start = datetime.now()


input_file = argv[1]
q_file = argv[2]
e_file = argv[3]
output_file = argv[4]

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


output = []
for line in data:
    str = ''
    for word, tag in line[2:]:
        str += word + '/' + tag + ' '
    output.append(str[:-1])


write_to_file(output_file, output)


print "Greedy hmm"

zman = datetime.now() - start
print(zman)