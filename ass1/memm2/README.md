## MEMM Tagger

# Greedy

python memm2/GreedyMaxEntTag.py ../data/ass1-tagger-train memm1/features_file 


# ConvertFeatures

python memm1/ConvertFeatures.py memm1/features_file memm1/feature_vecs_file memm1/feature_map_file


# Training 
Packages:
sklearn, pickle, scipy

python memm1/TrainSolver.py memm1/feature_vecs_file memm1/model