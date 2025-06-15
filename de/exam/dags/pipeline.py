from datetime import timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from pathlib import Path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1), # задержка между попытками
}

dag = DAG(
    'my_pipeline',
    default_args=default_args,
    description='Пример пайпдлайна',
    schedule='@daily',
    catchup=False,
)

# Пути к скриптам
SCRIPTS_DIR = f'{Path(__file__).parent.parent}/etl'


# 1 data_loader.py
data_loader = BashOperator(
    task_id='data_loader',
    bash_command=f'python3 {SCRIPTS_DIR}/data_loader.py',
    dag=dag,
)

# 2 transform.py
transform = BashOperator(
    task_id='transform',
    bash_command='python3 {{ params.scripts_dir }}/transform.py "{{ ti.xcom_pull(task_ids="data_loader", key="log_file") }}"',
    params={'scripts_dir': SCRIPTS_DIR},
    dag=dag,
)

# 3 train
train = BashOperator(
    task_id='train',
    bash_command='python3 {{ params.scripts_dir }}/train.py "{{ ti.xcom_pull(task_ids="data_loader", key="log_file") }}"',
    params={'scripts_dir': SCRIPTS_DIR},
    dag=dag,
)

# 4 evaluate.py
evaluate = BashOperator(
    task_id='evaluate',
    bash_command='python3 {{ params.scripts_dir }}/evaluate.py "{{ ti.xcom_pull(task_ids="data_loader", key="log_file") }}"',
    params={'scripts_dir': SCRIPTS_DIR},
    dag=dag,
)

# Определяем порядок выполнения
data_loader >> transform >> train >> evaluate
