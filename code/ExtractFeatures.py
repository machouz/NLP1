from utils import *
from datetime import datetime
from sys import argv

fname = argv[1]
output_file = argv[2]


def featureExtract(fname):
    text = read_data(fname)
    featured_data = []
    for line in text:
        featured_line = []
        for i in range(0, len(line)):
            features = get_features(i, line)
            featured_line.append(features)

        featured_data.append(featured_line)

    return featured_data


def get_features(index, line):
    features = {}

    if len(line[index]) == 2:  # Train
        current_word, current_tag = line[index]
        features["current_tag"] = current_tag
    else:  # Test
        current_word = line[index]

    previous_word, previous_tag = line[index - 1]
    pre_previous_word, pre_previous_tag = line[index - 2]
    features["current_word"] = current_word
    if len(current_word) >= 1:
        features["suffix1"] = current_word[-1]
        features["prefix1"] = current_word[0]

    if len(current_word) >= 2:
        features["suffix2"] = current_word[-2]
        features["prefix2"] = current_word[1]

    if len(current_word) >= 3:
        features["suffix3"] = current_word[-3]
        features["prefix3"] = current_word[2]

    if previous_word is not None:
        features["previous_word"] = previous_word

    if previous_tag is not None:
        features["previous_tag"] = previous_tag

    if pre_previous_word is not None:
        features["pre_previous_word"] = pre_previous_word

    if pre_previous_tag is not None:
        features["pre_previous_tag"] = pre_previous_tag
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
