# This file provides code which you may or may not find helpful.
# Use it if you want, or ignore it.
import random
import numpy as np
import nltk


def read_data(fname):
    data = []
    for line in file(fname):
        arr = ['***/STR', '***/STR']
        arr.extend(line.split(" "))
        data.append(map(lambda x: x.split('/'), arr))
    return data

def write_to_file(fname, data):
    np.savetxt(fname, data, delimiter='\n')


VBD
PRP$
CCL
WDT
JJ
WP
RP
$
:
(
FW
,
RB
WAD
NNS
NNP
WRB
T
NN
SYM
NNS
SYM
EMI
EMS
E
Net
#
VBN
PC
IN
DT
S
EX
MD
VMS
UH
UA
.
VBG
VBD
VBN
VBP
VBZ
NN
CD
.
)
JJ
:
VBP
PRP
``
B
CC
VB
PDT
CD
NNPS
WP$
JJS
JJR
NNPS
''
,
''
RB
DT
)
POS
TO
LS
NNP
VBZ
VB
ABC
JJR
``
RBS
RBR
STR
IN
RP
