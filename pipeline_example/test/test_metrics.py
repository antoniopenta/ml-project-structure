import warnings
warnings.simplefilter("ignore")
import unittest
import numpy as np
import pandas as pd
from utility.metrics import *
from utility.data_generation import *

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test




class TestMetrics(unittest.TestCase):

    @ignore_warnings
    def setUp(self):

        self.diminstance = 100
        self.clusters = 10
        self.n_features = 5
        self.random_state = 0
        self.dataframe ,self.label= generate_data(self.diminstance,self.clusters,self.n_features,self.random_state)

    def test_homogeneity(self):

        labels_random = self.label.copy()
        labels_semi_random = self.label.copy()

        np.random.shuffle(labels_random)

        choise_1 = np.random.choice(len(labels_semi_random), int(len(labels_semi_random)*0.1))
        choise_2 = np.random.choice(len(labels_semi_random), int(len(labels_semi_random) * 0.1))

        for item1,item2 in zip(choise_1,choise_2):
            tmp=labels_semi_random[item1]
            labels_semi_random[item1]=labels_semi_random[item2]
            labels_semi_random[item2]=tmp

        hom1=homegenity(self.label,labels_random)

        hom2 = homegenity(self.label, labels_semi_random)

        hom3 = homegenity(self.label, self.label)

        self.assertEqual(hom3,1,'same labels homogenity needs to be 1')

        self.assertGreaterEqual(hom2,hom1,'semi random should be not worst than full random')





