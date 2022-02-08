from typing import Optional

from fastapi import FastAPI

import pandas as pd

import json


app = FastAPI()

df = pd.DataFrame()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data/read/")
def read_file(name: str, separator: Optional[str] = ';'):
    global df
    if not df.empty:
      del df
      df = pd.DataFrame()
    path = "/datas/"
    df = pd.read_csv(path + name + '.csv', sep=separator)
    return True

@app.get("/data/columns/")
def get_columns():
    global df
    return df.columns.to_list()

@app.get("/data/len/")
def get_len():
    global df
    return len(df)

@app.get("/data/dtypes/")
def get_dtypes():
    global df
    return df.dtypes.to_json()
