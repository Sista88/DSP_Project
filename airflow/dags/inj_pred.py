import logging
from pendulum import today
from datetime import datetime
from datetime import timedelta
#from airflow import dag, task
import pandas as pd
from airflow.decorators import dag, task


#import sys
#sys.path.insert(0, '/Documents/Teja/Sem-3/Home_loan_example/UI with FastAPI')
from FastAPI.main2 import create_upload_file
#from airflow.utils.dates import days_ago

#from airflow.utils.dates import days_ago
#from main2 import create_upload_file


@dag(
    dag_id='ingest_data',
    description='Ingest data from a file to another DAG',
    tags=['dsp', 'data_ingestion'],
    schedule=timedelta(minutes=2),
    start_date=today().add(hours=-1)
)
def ingest_data():
    @task
    def get_data_to_ingest_from_local_file() -> pd.DataFrame:
        nb_rows = 5
        filepath = 'folderA/test (2).csv'
        input_data_df = pd.read_csv(filepath)
        logging.info(f'Extract {nb_rows} from the file {filepath}')
        data_to_ingest_df = input_data_df.sample(n=nb_rows)
        return data_to_ingest_df

    print(get_data_to_ingest_from_local_file())

    @task
    def save_data(data_to_ingest_df: pd.DataFrame) -> None:
        json_data = data_to_ingest_df.to_dict()
        #from main2 import create_upload_file
        data_to_ingest_df['Loan status'] = create_upload_file(json_data)
        filepath = f'folderB/{datetime.now().strftime("%Y-%M-%d_%H-%M-%S")}.csv'
        logging.info(f'Ingesting data in {filepath}')
        data_to_ingest_df.to_csv(filepath, index=False)

    # Task relationships
    data_to_ingest = get_data_to_ingest_from_local_file()
    save_data(data_to_ingest)


ingest_data_dag = ingest_data()