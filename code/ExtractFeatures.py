from utils import *
from datetime import datetime

fname = "../data/ass1-tagger-train"
output_file = "features"


def featureExtract(fname):
    train = read_data(fname)
    featured_data = []
    for line in train:
        featured_line = []
        first_word = line[0]
        first_word_features = get_features(first_word[0], first_word[1])
        featured_line.append(first_word_features)
        for previous_word_tag, current_word_tag in zip(line, line[1:]):
            features = get_features(current_word_tag[0], current_word_tag[1], previous_word_tag[0],
                                    previous_word_tag[1])

            featured_line.append(features)

        featured_data.append(featured_line)

    return featured_data


def get_features(current_word, current_tag, previous_word=None, previous_tag=None):
    features = {}
    features["current_word"] = current_word
    features["current_tag"] = current_tag
    features["suffix"] = current_word[-3:]
    if previous_tag is not None:
        features["previous_tag"] = previous_tag
    return features


def write_features_file(featured_data, output_file):
    data = []
    for line in featured_data:
        for featured_word in line:
            label = featured_word['current_tag']
            for key, value in featured_word.items():
                label += "\t" + key + "=" + value
            data.append(label)
    write_to_file(output_file, data)


if __name__ == '__main__':
    start = datetime.now()
    featured_data = featureExtract(fname)
    print(datetime.now() - start)
    write_features_file(featured_data, output_file)
    print(datetime.now() - start)
