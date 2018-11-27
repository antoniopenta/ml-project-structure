import pandas as pd
import numpy as np
import configparser
import os
import argparse




def read_values_fromfile_as_string (file , joinsuffix=','):
    with open(file) as file:
        rows = [item.strip()for item in file.readlines()]

    return joinsuffix.join(rows)







if __name__=='__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-excel_file', action='store',
                        dest='excel',
                        help='excel file with experiments definition', type=str, required=True)

    parser.add_argument('-sheet', action='store',
                        dest='sheet',
                        help='sheet number to use in the excel file', type=str, required=True)

    parser.add_argument('-experiment', action='store',
                        dest='experiment',
                        help=' the number of the experiment to consider', type=int, required=True)

    parser.add_argument('-conf_file', action='store',
                        dest='conf_file',
                        help='conf file to update', type=str, required=True)



    parser.add_argument('-experiment_attribute', action='store',
                        dest='experiment_atr',
                        help='sheet name in the excel', type=str, default='experiment')

    parser.add_argument('-multivalue_attribute_suffix', action='store',
                        dest='multivalue_atr_suffix',
                        help='sheet name in the excel', type=str, default='*')


    parser.add_argument('-join_multivalue', action='store',
                        dest='join_multivalue',
                        help='suffix used to join multivalue', type=str, default=',')

    parser.add_argument('-join_section', action='store',
                        dest='join_section',
                        help='suffix used to join value with section', type=str, default='@')

    args = parser.parse_args()


    excel_file = args.excel

    sheet_name = args.sheet

    expt_name = args.experiment

    conf_file = args.conf_file

    experiment_attribute = args.experiment_atr

    multivariable_attribute_suffix = args.multivalue_atr_suffix

    join_multivalue = args.join_multivalue

    join_section = args.join_section

    dataframe_dict = pd.read_excel(excel_file,sheet_name=None)


    assert sheet_name in dataframe_dict.keys(), 'the specified sheet %s is not in the excel file'%(sheet_name)


    dataframe = pd.read_excel(excel_file,sheet_name=sheet_name)

    assert experiment_attribute in dataframe.columns, 'there is not experiment attribute in the dataframe'


    assert not dataframe[
        experiment_attribute].isnull().values.any(), 'there is at least one value in experiment column which is null'


    dataframe_experiment = dataframe[dataframe[experiment_attribute]==expt_name]



    assert not dataframe_experiment.empty, 'the data frame selected with the experiment is empty'

    cols=[item for item in dataframe_experiment.columns if item!=experiment_attribute]
    config = configparser.ConfigParser()
    for row in dataframe_experiment.index:
        for col in cols:
            if len(col.split('.'))>0:
                col_conf = col.split('.')[0]
            else:
                col_conf = col
            value_section = dataframe_experiment.at[row, col]
            if not pd.isna(value_section):
                value_section = str(value_section)
                assert join_section in value_section, 'The value %s in row %s nd column %s is missing the section'%(str(value_section),str(row),str(col))
                assert len(value_section.split(join_section))==2, 'The value %s in row %s nd column %s is not well formatted ' % (str(value_section), str(row), str(col))
                value, section = value_section.split(join_section)
                if multivariable_attribute_suffix in col_conf:
                    col_conf = col_conf.split(multivariable_attribute_suffix)[1]
                    if os.path.exists(value):
                        value = read_values_fromfile_as_string(value,joinsuffix=join_multivalue)
                    else:
                        value=None
                if section not in config:
                    config[section] = {}
                config[section][col_conf] = str(value)
with open(conf_file, 'w') as file:
    config.write(file)

