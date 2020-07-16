#!/bin/sh
export deploy_github='airflow_deploy_github.py'
export deploy_github_bucket='gcs/bucket'
export dags_space='/airflow/dags'
gsutil -m rsync -r gs://${deploy_github_bucket}/${deploy_github} ${dags_space}
echo 'deploy_github.py deployed'

airflow variable --set airflow_deploy_github_parameters '{"repo" : "sample_repo","source" : "sample_folder/sample_dag.py","airport" : "sample_dag_folder"}'
echo 'variable set'