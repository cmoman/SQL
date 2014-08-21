#!/usr/bin/python
import MySQLdb as db

import numpy as np
import pandas as pd

from pandas.io.sql import frame_query

import matplotlib.pyplot as plt


database = db.connect('cit.tesla.local','python','python','cit2')
#data     = pd.io.sql.frame_query("SELECT * FROM work_logs WHERE started_at > '2014-08-01 00:00:00'", database)

data = frame_query("SELECT * FROM work_logs WHERE started_at > '2014-08-01 00:00:00'", database)


print data

#table=pivot_table(data, values='duration', index=['project_id','task_id'], columns='started_at', aggfunc=np.sum)

table=pd.pivot_table(data, values='duration', rows=['project_id','task_id'], cols='started_at', aggfunc=np.sum)

grouped=data.groupby(data['started_at'].map(lambda x:x.day))

writer = pd.ExcelWriter('output.xlsx')
table.to_excel(writer,'Sheet1')
grouped.to_excel(writer,'Sheet2')
writer.save()




print 'debug'