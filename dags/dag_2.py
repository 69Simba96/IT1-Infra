from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def check_dq(**kwargs):

    dag_run_conf = kwargs['dag_run'].conf
    file_name = dag_run_conf.get('file_name')
    source_row_count = dag_run_conf.get('source_row_count')

    if file_name or source_row_count is None:
        return

    source_row_count = int(source_row_count)
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    count_query = "SELECT count(*) FROM target WHERE name = %s;"
    result = pg_hook.get_first(count_query, parameters=(file_name,))
    target_row_count = result[0] if result else 0

    is_valid = (source_row_count == target_row_count)
    insert_query = """
        INSERT INTO dq_log (name, source_count, target_count, is_valid)
        VALUES (%s, %s, %s, %s);
    """
    pg_hook.run(insert_query, parameters=(file_name, source_row_count, target_row_count, is_valid))

    if not is_valid:
        raise ValueError("Data Quality check failed. Row counts do not match")


default_args = {
    'owner': 'airflow',
    "start_date": datetime(2026, 6, 1),
}

with DAG(
    dag_id='data_quality_check',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    dq_task = PythonOperator(
        task_id='validate_row_counts',
        python_callable=check_dq,
    )