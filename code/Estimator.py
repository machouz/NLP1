from utils import *
import re
from datetime import datetime

# Dictionary that give a compiled regex for each signature
signatures_regex = {"^ed": re.compile("\w+ed$"),
                    "^s": re.compile("\w+s$"),
                    "^ing": re.compile("\w+ing$"),
                    "^ent": re.compile("\w+ent$"),
                    "^Aa": re.compile("[A-Z][a-z]+"),
                    "^ion": re.compile("\w+ion$"),
                    "^ity": re.compile("\w+ity$"),
                    }


def replace_signature(word):
    for signature, regex in signatures_regex.items():
        if regex.match(word):
            return signature
    return word


class Estimator:
    tag_trigram = {}
    tag_bigram = {}
    tag_unigram = {}
    word_tag = {}

    def __init__(self, gamma1=None, gamma2=None, gamma3=None):
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.gamma3 = gamma3

    def unknown_signature(self, threshold_unk):
        for sample, count in self.word_tag.items():
            word, tag = sample.split(" ")
            if count <= threshold_unk:
                sign = replace_signature(word)
                del self.word_tag[sample]
                if sign != word:
                    self.word_tag[sign + " " + tag] = self.word_tag.get(sign + " " + tag, 0) + count
                else:
                    self.word_tag["*UNK*" + " " + tag] = self.word_tag.get("*UNK*" + " " + tag, 0) + count

    def addQLine(self, a, b, c=None):
        self.tag_unigram[a] = self.tag_unigram.get(a, 0) + 1
        self.tag_bigram[a + " " + b] = self.tag_bigram.get(a + " " + b, 0) + 1
        if c is None:
            self.tag_unigram[b] = self.tag_unigram.get(b, 0) + 1
        else:
            self.tag_trigram[a + " " + b + " " + c] = self.tag_trigram.get(a + " " + b + " " + c, 0) + 1

    def addELine(self, x):
        word, tag = x
        self.word_tag[word + " " + tag] = self.word_tag.get(word + " " + tag, 0) + 1

    def getQ(self, t1, t2, t3):
        tri = 0
        bi = 0
        if t1 + " " + t2 in self.tag_bigram:
            tri = self.gamma1 * self.tag_trigram.get(t1 + " " + t2 + " " + t3, 0) / self.tag_bigram.get(t1 + " " + t2)

        if t2 in self.tag_unigram:
            bi = self.gamma2 * self.tag_bigram.get(t2 + " " + t3, 0) / self.tag_unigram.get(t2, 0)

        uni = self.gamma3 * self.tag_unigram.get(t3, 0) / sum(self.tag_unigram.itervalues())
        return tri + bi + uni

    def getE(self, word, tag):
        sign = replace_signature(word)
        if sign + " " + tag in self.word_tag:
            return float(self.word_tag[sign + " " + tag]) / self.tag_unigram[tag]
        return self.word_tag.get("*UNK*" + " " + tag, 0.0) / self.tag_unigram[tag]

    def qFile(self, ):
        data = []
        for key, label in self.tag_unigram.items():
            data.append(key + "\t" + str(label))
        for key, label in self.tag_bigram.items():
            data.append(key + "\t" + str(label))
        for key, label in self.tag_trigram.items():
            data.append(key + "\t" + str(label))
        write_to_file("q.mle", data)
        return data

    def eFile(self, ):
        data = []
        for key, label in self.word_tag.items():
            data.append(key + "\t" + str(label))
        write_to_file("e.mle", data)
        return data