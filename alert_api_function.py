import os, json, logging
from airflow.operators.http_operator import SimpleHttpOperator


'''
it is a function to call api which may be implemented for failure callback
dag = DAG(
    'on_failure_callback': alert_api_function
)
'''

# below configuration may set to be acquired from an external file
json_path = '/home/alert_api_request.json' # location of the request json file
test_http = 'http://dummy.restapiexample.com/https' # a dummy rest api, '/https at the end enables to call via https instead of http
test_http_endpoint = '/create'
os.environ['AIRFLOW_CONN_TEST_HTTP'] = test_http

# alert api function
def alert_api_function(context):
    response = json.load(open(json_path, 'r'))
    # get info from dag
    text_description = '''
        Airflow : airflow
        DAG : {dag_id}
        Task : {task_id}
        error : {error}
    '''.format(dag_id = context['task_instance'], task_id = context['task_instance'].task_id, error = context['exception'].args)
    response['text'] = text_description[:1024]
    return SimpleHttpOperator(
        task_id = 'alert_api',
        method = 'POST',
        http_conn_id = 'test_http',
        endpoint = test_http_endpoint,
        data = response,
        log_response = True,
        # extra_option = {'verify': False} # it is to disable ssl verification
    ).execute(context)