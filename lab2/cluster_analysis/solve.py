#-*- coding:utf-8 -*-
from sklearn.cluster import KMeans


class Solution():
    def solve(self, X):
        kmodel = KMeans(n_clusters=12)
        result = kmodel.fit_predict(X)
        return result

        pass


