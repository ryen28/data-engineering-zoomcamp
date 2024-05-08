#!/usr/bin/env python
# coding: utf-8

from time import time

import pandas as pd
from sqlalchemy import create_engine # need to import so we can create a connection between this notebook and the postgres db

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000) # allows you to chunk the csv using iterator.
df = next(df_iter)

# convert the pickup and dropoff cols to datetime objects
df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace') # just add the columns


while True:
    t_start = time()

    df = next(df_iter)

    df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
    df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end-t_start))
