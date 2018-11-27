import luigi
import configparser
import pandas as pd
from utility.data_generation import generate_data
from framework.cluster import  KMeansAlgo0
from utility.metrics import *
import numpy as np

class GenerateData(luigi.Task):
    conf = luigi.Parameter()

    def requires(self):
        return []

    def run(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        diminstance = int(float(config['data_generation']['diminstance']))
        clusters = int(float(config['data_generation']['clusters']))
        n_features = int(float(config['data_generation']['n_features']))
        random_state = int(float(config['data_generation']['random_state']))

        data,labels = generate_data(diminstance,clusters,n_features,random_state)

        dataframe = pd.DataFrame(data, columns=[ str(item) for item in range(0,n_features,1)])

        dataframe.to_csv(self.output()[0].path, index=False)

        labelsframe =pd.DataFrame(labels,columns=['label'])

        labelsframe.to_csv(self.output()[1].path,index=False)


    def output(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        return [luigi.LocalTarget(config['file']['file_dataframe']),
                luigi.LocalTarget(config['file']['file_label_true'])]




class KMeansAlgo0Module(luigi.Task):
    conf = luigi.Parameter()

    def requires(self):
        return [GenerateData(self.conf)]


    def run(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        k = int(float(config['kmeansalgo0']['k']))

        dataframe = pd.read_csv(self.input()[0][0].path)

        data = dataframe.values

        model = KMeansAlgo0(k)

        model.fit(data)

        labels = pd.DataFrame(model.getLabel(),columns=['label_cluster'])

        labels.to_csv(self.output()[0].path,index=False)



    def output(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        return [luigi.LocalTarget(config['file']['file_label_predicted'])]




class LabelForMetricsFileChecker(luigi.ExternalTask):
    conf = luigi.Parameter()

    def output(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        return  [luigi.LocalTarget(config['file']['file_label_true']),luigi.LocalTarget(config['file']['file_label_predicted'])]




class ClusterMetrics(luigi.Task):
    conf = luigi.Parameter()

    def requires(self):
        return LabelForMetricsFileChecker(self.conf)



    def run(self):
        config = configparser.ConfigParser()
        config.read(self.conf)

        label_true = pd.read_csv(self.input()[0].path)
        label_predicted = pd.read_csv(self.input()[1].path)

        label_true = label_true.values.flatten()
        label_predicted = label_predicted.values.flatten()

        #import pdb
        #pdb.set_trace()

        value_hom = homegenity(label_true,label_predicted)

        value_comple = completeness(label_true, label_predicted)

        df=pd.DataFrame([[value_comple,value_hom]],columns=['completeness','homogenity'])

        df.to_csv(self.output().path,index=False)


    def output(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        return luigi.LocalTarget(config['file']['file_metrics'])







