import pandas as  pd
from prophet import Prophet
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from logger import log
from urllib.parse import quote_plus

load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
engine = create_engine(f'mysql+pymysql://{db_user}:{quote_plus(db_password)}@{db_host}/{db_name}')

def get_sales_data():
    query = "SELECT `Transaction Date`, SUM(Sales) as total_sales FROM transactions GROUP BY `Transaction Date`"
    df = pd.read_sql(query, con=engine)
    df.rename(columns={'Transaction Date': 'ds', 'total_sales': 'y'}, inplace=True)
    return df

def run_forecast(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def save_forecast_to_mysql(forecast):
    forecast.to_sql('sales_forecast', con=engine, if_exists='replace', index=False)
    log(f"Saved {len(forecast)} forecast rows to MySQL.")

if __name__ == "__main__":
    log("Starting sales forecasting...")
    sales_data = get_sales_data()
    forecast = run_forecast(sales_data)
    save_forecast_to_mysql(forecast)
    log("Forecasting complete!")