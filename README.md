
Easy and powerful template for ML projects



## Prerequisites

```
pip install -r requirements.txt
```


## Getting Started
The following command creates  a structure specified in template.json for your ML projects
```
python build.py -dir project_example/ -template_file  template.json
```
An example of  structure that can be defined in the template.json

```json
{
  "num_algorithm": 2,
  "num_training_testing_validation": 2,
  "directory_training_suffix": "training",
  "datasets": [
    "dataset_1"
  ],
  "main_directories": [
    "config_pipelines",
    "data_experiments",
    "@framework",
    "@jupyter",
    "@luigi_pipeline"
  ],
  "sub_directories": [
    {
      "father": "config_pipelines",
      "dirs": [
        "directory_algoritm_suffix*num_algorithm",
        "data_generation",
        "data_processing",
        "metrics"
      ]
    }
  ]
}
```
 * @ in "@framework" is used to specify if the folder is a python module
*  num_algorithm is used to specify how many algorithms you would like to test
 * "directory_algoritm_suffix*num_algorithm" is used to generate multiple folders where the * suffix(directory_algoritm_suffix) and the number (num_algorithm) are specified in the template too.



## Luigi Pipeline for experiments

In the folder pipeline_example, there is an dummy example of how to use Luigi pipeline for evaluating a KMeans algorithm.

The main idea is to define the experiments using excel as follows:


| experiment | diminstance         | clusters           | n_features        | random_state      | file_dataframe                                           | file_label_true                                           | k              | file_label_predicted                                                   | file_metrics                                          |
|------------|---------------------|--------------------|-------------------|-------------------|----------------------------------------------------------|-----------------------------------------------------------|----------------|------------------------------------------------------------------------|-------------------------------------------------------|
| 1          | 100@data_generation | 10@data_generation | 5@data_generation | 0@data_generation | data_experiments/data_generation/file_dataframe.csv@file | data_experiments/data_generation/file_label_true.csv@file | 10@kmeansalgo0 | data_experiments/algorithm0/file_label_predicted_algorithm0_1.csv@file | data_experiments/metrics/metrics_algorithm_1.csv@file |
| 2          | 100@data_generation | 10@data_generation | 5@data_generation | 0@data_generation | data_experiments/data_generation/file_dataframe.csv@file | data_experiments/data_generation/file_label_true.csv@file | 20@kmeansalgo0 | data_experiments/algorithm0/file_label_predicted_algorithm0_2.csv@file | data_experiments/metrics/metrics_algorithm_2.csv@file |
| 3          | 100@data_generation | 10@data_generation | 5@data_generation | 0@data_generation | data_experiments/data_generation/file_dataframe.csv@file | data_experiments/data_generation/file_label_true.csv@file | 30@kmeansalgo0 | data_experiments/algorithm0/file_label_predicted_algorithm0_3.csv@file | data_experiments/metrics/metrics_algorithm_3.csv@file |More info about Luigi can be found here : https://github.com/spotify/luigi


Each row is an experiment
Each column is an attribute of the configuration file
@ is used to defined the key of the dictorany in the configuration file. For example :

| experiment | k              |
|------------|----------------|
| 1          | 10@kmeansalgo0 |

becomes in a configuration file :

```
[kmeansalgo0]
k = 30
```

The extraction of the configuration file from the excel file is done using the python script
```update_config_files.py```

The bash file ```exp_cluster.sh``` is used to run the pipeline:

This is used to create the configuration file using the data defined in the experiment 1
```
python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 1 -conf_file config_pipelines/data_generation/evaluation_pipeline.conf
```
 Then the pipeline is lunched using the configuration file created above:
```
luigi --module luigi_pipeline.evaluation_pipeline   GenerateData  --conf config_pipelines/data_generation/evaluation_pipeline.conf  --local-scheduler --no-lock
```

## Authors

     **Antonio Penta