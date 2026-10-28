import pandas as pd
import sqlalchemy as sql
from sqlalchemy.engine import URL
import os


def extract(filepath):
    print("1. Извлечение.." )
    df = pd.read_excel(filepath)
    return df


def transform_data(df):
    print("2. Трансформация")
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    return df


def load(df):
    print("3. Загрузка данных...")
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5433')

    url = URL.create(
        drivername='postgresql+psycopg2',
        username='postgres',
        password='postgres',
        host=db_host,
        port=db_port,
        database='crm'
    )
    engine = sql.create_engine(url)

    df.to_sql('retail_clean', engine, if_exists='replace', index=False)
    print("ETL успешно!")


if __name__ == "__main__":
    raw_df = extract('data/Online Retail.xlsx')
    clean_df = transform_data(raw_df)
    load(clean_df)