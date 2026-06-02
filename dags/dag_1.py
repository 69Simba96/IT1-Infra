import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

INPUT_DIR = 'C:/Users/Katy/IT1-Infra/airflow_input/'

def read_file(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')

    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        return None

    all_files = os.listdir(INPUT_DIR)
    if not all_files:
        print('No files found')
        return None

    processed_query = "SELECT name FROM processed_files;"
    processed_files = {row[0] for row in pg_hook.get_records(processed_query)}

    file_to_process = None
    for name in all_files:
        if name not in processed_files:
            file_to_process = name
            break

    if file_to_process is None:
        print('All files were processed')
        return None

    file_path = os.path.join(INPUT_DIR, file_to_process)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    source_row_count = len(lines)

    with pg_hook.get_conn() as conn:
        with conn.cursor() as cursor:
            for row in lines:
                cursor.execute("INSERT INTO target (name, data) VALUES (%s, %s);", (file_to_process, row))
            cursor.execute("INSERT INTO processed_files (name) VALUES (%s);", (file_to_process,))
        conn.commit()

    kwargs['ti'].xcom_push(key='processed_file_name', value=file_to_process)
    kwargs['ti'].xcom_push(key='source_row_count', value=source_row_count)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        dag_id='etl_process',
        default_args=default_args,
        schedule_interval='0 * * * *',
        catchup=False
) as dag:
    etl_process_task = PythonOperator(
        task_id='etl_process_task',
        python_callable=read_file
    )

    dq = TriggerDagRunOperator(
        task_id='check_dq',
        trigger_dag_id='data_quality_check',
        conf={
            "file_name": "{{ ti.xcom_pull(task_ids='etl_process_task', key='processed_file_name') }}",
            "source_row_count": "{{ ti.xcom_pull(task_ids='etl_process_task', key='source_row_count') }}"
        },
        failed_states=["failed"],
        allowed_states=["success"]
    )


    etl_process_task >> dq
