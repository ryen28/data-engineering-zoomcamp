#!/usr/bin/env python
# coding: utf-8

import argparse
from time import time

import pandas as pd
from sqlalchemy import create_engine # need to import so we can create a connection between this notebook and the postgres db


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name

    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000) # allows you to chunk the csv using iterator.
    df = next(df_iter)

    # convert the pickup and dropoff cols to datetime objects
    df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
    df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace') # just add the columns

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    while True:
        t_start = time()

        df = next(df_iter)

        df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
        df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end-t_start))





parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

parser.add_argument('user', help='user name for postgres')
parser.add_argument('password', help='password for postgres')
parser.add_argument('host', help='host for postgres')
parser.add_argument('port', help='port for postgres')
parser.add_argument('db', help='database name for postgres')
parser.add_argument('table-name', help='name of the table where we will write the results to')
parser.add_argument('url', help='url of the csv file')

args = parser.parse_args()
print(args.accumulate(args.integers))
