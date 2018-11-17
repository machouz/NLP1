from utils import *
from datetime import datetime

features_file = "features"
feature_vecs_file = "feature_vecs"
feature_map_file = "feature_map"

feat2id = file_to_dic(feature_map_file)


def featureConvert(fname):
    features_id = {}
    i = 0
    data = []
    for line in file(fname):
        line = line[:-1].split("\t")

        label = feat2id[line[0]]
        vec = [label]
        for feature in line[1:]:
            if feature not in features_id:
                features_id[feature] = str(i) + ":1"
                i += 1

            vec.append(features_id[feature])
        data.append(vec)

    write_to_file(feature_vecs_file, data)

    return data


if __name__ == '__main__':
    start = datetime.now()
    data = featureConvert(features_file)
    print(datetime.now() - start)
