from airflow.models import DAG, Variable
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

'''
Variables
----------
repo: example url as https://<token>@github.com/leeeeeeewii/Airflow-Practice.git
source: target file(s) in repo to be updated, leave space to update the entire repo
airport: target folder to place dag, leave space to update repo in airflow dag folder
----------
sample json input
{
    "repo" : "sample_repo",
    "source" : "sample_folder/sample_dag.py",
    "airport" : "sample_dag_folder"
}
'''

airflow_deploy_github_parameters = Variable.get('airflow_deploy_github_parameters', deserialize_json=True)
temp = '/tmp/landing'

default_args = {
    'owner': 'airflow',
    'depend_on_past': False,
    'start_date': datetime(2020,7,1),
    'retries': 1,
}

dag = DAG(
    dag_id = 'airflow_deploy_github',
    default_args = default_args,
    schedule_interval = None,
    catup = False,
)

Prepare_landing = BashOperator(
    task_id = 'Prepare_landing',
    bash_command = 'rm -rf {}'.format(temp),
    dag = dag,
)

Clone_repo = BashOperator(
    task_id = 'Clone_repo',
    bash_command = 'git clone {0} {1}'.format(airflow_deploy_github_parameters['repo'], temp),
    dag = dag,
)

Deploy_dag = BashOperator(
    task_id = 'Deploy_dag',
    bash_command = 'rysnc -r {0}{1} {2}'.format(temp, airflow_deploy_github_parameters['source'], airflow_deploy_github_parameters['airport']),
    dag = dag,
)

Clear_space = BashOperator(
    task_id = 'Clear_space',
    bash_command = 'rm -rf {}'.format(temp),
    dag = dag,
)

Auth_setup = BashOperator(
    task_id = 'Auth_setup',
    bash_command = 'cd {} & airflow sync_perm'.format(airflow_deploy_github_parameters['airport']),
    dag = dag,
)

Prepare_landing >> Clone_repo >> Deploy_dag >> Clear_space >> Auth_setup