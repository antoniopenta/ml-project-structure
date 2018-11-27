from sklearn.cluster import KMeans


class KMeansAlgo0:



    def __init__(self,k):

      self.k = k


    def fit(self,X):
        self.clustermodel = KMeans(n_clusters=self.k,).fit(X)



    def getLabel(self):
        assert self.clustermodel is not None, 'before getting the label, you need to run the fit method'
        return self.clustermodel.labels_



    def getCentroids(self):
        assert self.clustermodel is not None, 'before getting the centrods, you need to run the fit method'
        return self.clustermodel.cluster_centers_




