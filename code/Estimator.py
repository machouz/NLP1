from utils import *
import re

# Dictionary that give a compiled regex for each signature
signatures_regex = (["^0-9", re.compile('\w*\d+\w*')],
                    ["^ed", re.compile("\w+ed$")],
                    ["^ing", re.compile("\w+ing$")],
                    ["^ion", re.compile("\w+ion$")],
                    ["^ity", re.compile("\w+ity$")],
                    ["^able", re.compile("\w+able$")],
                    ["^ent", re.compile("\w+ent$")],
                    ["^s", re.compile("\w+s$")],
                    ["^ly", re.compile("\w+ly$")],
                    ["^A-Z", re.compile("[A-Z]+$")],
                    )


def replace_signature(word):
    for signature, regex in signatures_regex:
        if regex.match(word):
            return signature
    return word


class Estimator:
    tag_trigram = {}
    tag_bigram = {}
    tag_unigram = {}
    num_words = 0
    tag_unigram_events = {}
    word_tag = {}

    def __init__(self, gamma1=0.1, gamma2=0.4, gamma3=0.5):
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.gamma3 = gamma3

    def load_from_file(self, q_file, e_file):
        self.word_tag = {}
        self.tag_unigram_events = {}
        for line in file(e_file):
            key, count = line[:-1].split('\t')
            word, tag = key.split(" ")
            self.tag_unigram_events[tag] = self.tag_unigram_events.get(tag, 0) + 1
            if word not in self.word_tag:
                self.word_tag[word] = {}
            self.word_tag[word][tag] = int(count)

        self.num_words = 0
        for line in file(q_file):
            key, value = line[:-1].split('\t')
            gram = key.split()
            if len(gram) == 3:
                self.tag_trigram[key] = int(value)
            elif len(gram) == 2:
                self.tag_bigram[key] = int(value)
            else:
                self.num_words += 1
                self.tag_unigram[key] = int(value)

    def unknown_signature(self, threshold_unk=0):
        self.tag_unigram_events = self.tag_unigram.copy()
        for word, dic in self.word_tag.items():
            for tag, count in dic.items():
                sign = replace_signature(word)
                if sign != word:
                    self.tag_unigram_events[tag] = self.tag_unigram_events.get(tag, 0) + 1
                    if sign not in self.word_tag:
                        self.word_tag[sign] = {}
                    self.word_tag[sign][tag] = self.word_tag[sign].get(tag, 0) + count

    def get_best_tag(self, a, b, c):
        t1, t2 = a[1], b[1]
        max_value = 0
        t3 = ""

        for x in self.tag_unigram:
            value = self.getQ(t1, t2, x) * self.getE(c, x)
            if value > max_value:
                max_value = value
                t3 = x
        return t3

    def addQLine(self, a, b, c=None):
        self.tag_unigram[a] = self.tag_unigram.get(a, 0) + 1
        self.tag_bigram[a + " " + b] = self.tag_bigram.get(a + " " + b, 0) + 1
        if c is None:
            self.tag_unigram[b] = self.tag_unigram.get(b, 0) + 1
        else:
            self.tag_trigram[a + " " + b + " " + c] = self.tag_trigram.get(a + " " + b + " " + c, 0) + 1

    def addELine(self, x, dev=False):
        word, tag = x
        if word not in self.word_tag:
            if dev:
                word = '*UNK*'
            if word not in self.word_tag:
                self.word_tag[word] = {}
        if tag not in self.word_tag[word]:
            self.word_tag[word][tag] = 0

        self.num_words += 1
        self.word_tag[word][tag] += 1

    def getQ(self, t1, t2, t3):
        tri = 0
        bi = 0

        if t1 + " " + t2 + " " + t3 in self.tag_trigram:
            tri = float(self.tag_trigram.get(t1 + " " + t2 + " " + t3, 0)) / self.tag_bigram.get(t1 + " " + t2, 0)

        if t2 + " " + t3 in self.tag_bigram:
            bi = float(self.tag_bigram.get(t2 + " " + t3, 0)) / self.tag_unigram.get(t2, 0)

        uni = float(self.tag_unigram.get(t3, 0)) / self.num_words
        return self.gamma1 * tri + self.gamma2 * bi + self.gamma3 * uni

    def getE(self, word, tag):
        if word in self.word_tag:
            return float(self.word_tag[word].get(tag, 0)) / self.tag_unigram_events.get(tag, 1)

        sign = replace_signature(word)
        if sign in self.word_tag:
            return float(self.word_tag[sign].get(tag, 0)) / self.tag_unigram_events.get(tag, 1)

        return float(self.word_tag["*UNK*"].get(tag, 0)) / self.tag_unigram_events.get(tag, 1)



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
        for word, dic in self.word_tag.items():
            for tag, count in dic.items():
                data.append(word + " " + tag + "\t" + str(count))
        write_to_file("e.mle", data)
        return data
