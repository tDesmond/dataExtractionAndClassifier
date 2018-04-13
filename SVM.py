#
#   tydes
#   19/03/2018
#

import numpy as np
from sklearn import preprocessing, cross_validation, neighbors, svm
import pandas as pd
from sklearn_porter import Porter
import matplotlib.pyplot as plt

df = pd.read_csv('trainingDataFinal.csv')
df.replace('?', 0, inplace=True)
df.replace("", 0, inplace=True)

X = np.array(df.drop(['Result'], 1))
y = np.array(df['Result'])
print(list(df)[:-1])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1)

clf = svm.LinearSVC()

clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print(confidence)

print(clf.coef_)
print(clf.verbose)
print(clf.fit(X, y))

# def plot_coefficients(classifier, feature_names, top_features=6):
#     coef = classifier.coef_.ravel()
#     top_positive_coefficients = np.argsort(coef)[-top_features:]
#     top_negative_coefficients = np.argsort(coef)[:top_features]
#     top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
#     # create plot
#     plt.figure(figsize=(15, 5))
#     colors = ["red" if c < 0 else "blue" for c in coef[top_coefficients]]
#     plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
#     feature_names = np.array(feature_names)
#     plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha="right")
#     plt.show()


# plot_coefficients(clf, list(df)[:-1])

# example_measures = np.array([[0.7, 0.5, 0.4, 0.02, 0.05, 0.005]])
# example_measures = example_measures.reshape(len(example_measures), -1)
# prediction = clf.predict(example_measures)
# print(prediction)


porter = Porter(clf, language='java')
output = porter.export(embed_data=True)
print(output)

w = clf.coef_[0][0]
print(w)
print(X_train)
print(X_train[:, 0])
print(y_train)

# plt.plot(X_train[:, 0],y_train)
# plt.scatter
# plt.show()
