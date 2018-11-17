from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
import pickle

feature_vecs_file = "feature_vecs"
model_file = "model"

X_train, Y_train = load_svmlight_file(feature_vecs_file)
model = LogisticRegression()
model.fit(X_train, Y_train)
# save the model to disk
pickle.dump(model, open(model_file, 'wb'))
