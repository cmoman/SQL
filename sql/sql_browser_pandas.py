#!/usr/bin/python
#import pandas as pd
import pandas.io.sql as psql
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqldb://python:python@cit.tesla.local/cit2', echo=False)
f = psql.read_frame('SELECT * FROM work_logs', engine, index_col = 'ID')

engine2 = create_engine



print f

