
import glob
import pandas as pd
import os
import argparse












if __name__=='__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-pm', action='store',
                        dest='path_metric',
                        help='path where the results to combine are saved', type=str, required=True)

    parser.add_argument('-o', action='store',
                        dest='path_save',
                        help=' where to save the results', type=str, required=True)


    args = parser.parse_args()

    path_metrics = args.path_metric
    path_save = args.path_save

    #path ='data_experiments/'
    #'all_metric_labels.csv'
    #print(os.path.join(path_metrics,'**/metrics_*'))

    list_df = []

    for filename in glob.glob(os.path.join(path_metrics,'**/metrics_*'), recursive=True):

        df = pd.read_csv(filename)
        df['name file']=[ os.path.basename(filename) for item in range(0,df.shape[0],1)]
        list_df.append(df)
    assert len(list_df)>0, 'the list of data frame to combine is empty'

    result = pd.concat(list_df)

    result.to_csv(path_save,index=None)
