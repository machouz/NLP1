from ass1.utils import *
from datetime import datetime
from sys import argv

fname = argv[1]
output_file = argv[2]


def featureExtract(fname):
    text = read_data(fname)
    featured_data = []
    for line in text:
        featured_line = []
        for i in range(2, len(line)):
            features = get_features(i, line)
            featured_line.append(features)

        featured_data.append(featured_line)

    return featured_data


def get_features(index, line):
    features = {}
    current_word, current_tag = line[index]
    features["current_tag"] = current_tag
    features["current_word"] = current_word

    if index > 0:
        previous_word, previous_tag = line[index - 1]
        features["previous_word"] = previous_word
        features["previous_tag"] = previous_tag

    if index > 1:
        pre_previous_word, pre_previous_tag = line[index - 2]
        features["pre_previous_tag"] = pre_previous_tag
        features["pre_previous_word"] = pre_previous_word

    if len(line) > index + 1:
        next_word = line[index + 1][0]
        features["next_word"] = next_word

    if len(line) > index + 2:
        next_next_word = line[index + 2][0]
        features["next_next_word"] = next_next_word

    return features


def write_features_file(featured_data, output_file):
    data = []
    for line in featured_data:
        for featured_word in line:
            label = featured_word['current_tag']
            del featured_word['current_tag']
            for key, value in featured_word.items():
                label += " " + key + "=" + value
            data.append(label)
    write_to_file(output_file, data)


if __name__ == '__main__':
    start = datetime.now()
    featured_data = featureExtract(fname)
    print(datetime.now() - start)
    write_features_file(featured_data, output_file)
    print(datetime.now() - start)
