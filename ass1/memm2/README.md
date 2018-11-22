## MEMM Tagger

# Greedy

python ass1/memm2/GreedyMaxEntTag.py data/ass1-tagger-train ass1/memm1/features_file 


# ConvertFeatures

python ass1/memm1/ConvertFeatures.py ass1/memm1/features_file ass1/memm1/feature_vecs_file ass1/memm1/feature_map_file


# Training 
Packages:
sklearn, pickle, scipy

python ass1/memm1/TrainSolver.py ass1/memm1/feature_vecs_file ass1/memm1/model




