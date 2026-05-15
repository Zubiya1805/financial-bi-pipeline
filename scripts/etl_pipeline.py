import pandas as pd
import os   
from sqlalchemy import create_engine
import pymysql
from logger import log
import shutil
from dotenv import load_dotenv
import numpy as np
from urllib.parse import quote_plus

load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
engine = create_engine(f'mysql+pymysql://{db_user}:{quote_plus(db_password)}@{db_host}/{db_name}')

def get_new_files():
    raw_dir = 'data/raw'
    processed_dir = 'data/archive'
    all_files = os.listdir(raw_dir)
    processed_files = os.listdir(processed_dir)
    new_files = [f for f in all_files if f not in processed_files and f.endswith('.csv')]
    return new_files

def validate_and_clean(df):
    rows_before = len(df)
    df = df.dropna()
    rows_after = len(df)
    log(f"Removed {rows_before - rows_after} rows with missing values.")
    
    df = df.drop_duplicates('Transaction ID')
    log(f"Removed {rows_before - df.shape[0]} duplicate rows.")
    
    df = df[df['Sales'] > 0]
    log(f"Removed rows with non-positive sales. Remaining rows: {len(df)}")

    df= df[(df['Discount']>=0) & (df['Discount']<=1)]
    log(f"Removed rows with invalid discount values. Remaining rows: {len(df)}")
    
    return df

def flag_anomalies(df):
    df['is_anomaly'] = np.where((df['Discount'] > 0.35) | (df['Profit'] < 0), 1, 0)
    log(f"Flagged {df['is_anomaly'].sum()} anomalies based on discount and profit.")
    return df

    df.to_sql('transactions', con=engine, if_exists='append', index = False)

def load_to_mysql(df):
    try:
        df.to_sql('transactions', con=engine, if_exists='append', index=False)
        log(f"Loaded {len(df)} records into MySQL.")
    except Exception as e:
        log(f"Error loading data to MySQL: {e}")
        
def archive_file(filename):
    shutil.move(os.path.join('data', 'raw', filename), os.path.join('data', 'archive', filename))
    log(f"Archived file: {filename}")
    
def run_pipeline():
    log("ETL Pipeline started")
    new_files = get_new_files()
    if not new_files:
        log("No new files to process. Pipeline finished.")
        
    for filename in new_files:
        log(f"Processing file: {filename}")
        try:
            df = pd.read_csv(os.path.join('data', 'raw', filename))
            df = validate_and_clean(df)
            df = flag_anomalies(df)
            load_to_mysql(df)
            archive_file(filename)
        except Exception as e:
            log(f"Error processing file {filename}: {e}")
    log("ETL Pipeline finished")
    
if __name__ == "__main__":
    run_pipeline()