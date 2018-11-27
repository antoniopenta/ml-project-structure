#!/usr/bin/env bash


#!/usr/bin/env bash
export AntonioPath=/Users/antonio.penta/Documents/workspace/python/datascience_project_template
export PYTHONPATH=$PYTHONPATH:$AntonioPath




# delete the previous results
find data_experiments/  name "*.csv" -type f -delete
find data_experiments/  name "*.txt" -type f -delete
find config_pipelines/  name "*.conf" -type f -delete

python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 1 -conf_file config_pipelines/data_generation/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline   GenerateData  --conf config_pipelines/data_generation/evaluation_pipeline.conf  --local-scheduler --no-lock

python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 1 -conf_file config_pipelines/algorithm0/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline KMeansAlgo0Module  --conf config_pipelines/algorithm0/evaluation_pipeline.conf  --local-scheduler --no-lock
python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 1 -conf_file config_pipelines/metrics/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline ClusterMetrics  --conf config_pipelines/metrics/evaluation_pipeline.conf  --local-scheduler --no-lock

python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 2 -conf_file config_pipelines/algorithm0/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline KMeansAlgo0Module  --conf config_pipelines/algorithm0/evaluation_pipeline.conf  --local-scheduler --no-lock
python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 2 -conf_file config_pipelines/metrics/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline ClusterMetrics  --conf config_pipelines/metrics/evaluation_pipeline.conf  --local-scheduler --no-lock


python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 3 -conf_file config_pipelines/algorithm0/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline KMeansAlgo0Module  --conf config_pipelines/algorithm0/evaluation_pipeline.conf  --local-scheduler --no-lock
python scripts/update_config_files.py -excel_file experimental_settings/experiments_metafile.xlsx -sheet exp_cluster -experiment 3 -conf_file config_pipelines/metrics/evaluation_pipeline.conf
luigi --module luigi_pipeline.evaluation_pipeline ClusterMetrics  --conf config_pipelines/metrics/evaluation_pipeline.conf  --local-scheduler --no-lock



# conbine all results
python scripts/combine_metrics.py -pm data_experiments/metrics/ -o data_experiments/metrics//metrics_all.csv