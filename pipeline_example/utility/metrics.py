
import numpy as np
from sklearn import metrics




def homegenity(label_true, label_predict):

    return metrics.homogeneity_score(label_true,label_predict)


def completeness(label_true, label_predict):


    return metrics.completeness_score(label_true,label_predict)