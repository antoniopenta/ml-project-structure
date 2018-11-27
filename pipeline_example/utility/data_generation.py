

from sklearn.datasets.samples_generator import make_blobs





def generate_data(diminstance, clusters, n_features,
                           random_state):

    data, labels = make_blobs(diminstance, centers=clusters, n_features=n_features,
                              random_state=random_state)

    return data,labels



