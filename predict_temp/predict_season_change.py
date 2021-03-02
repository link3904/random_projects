import sys
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import time

start_dt = date(2000,1,1)
end_dt = date.today() - timedelta(days=1)
tgt_dt = start_dt
df = pd.DataFrame()

while tgt_dt <= end_dt:
    dt_str = str(tgt_dt)[:7]
    print(dt_str)
    for attempt in range(10):
        try:
            url = f'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466910&stname=%25E9%259E%258D%25E9%2583%25A8&datepicker={dt_str}'
            tmp = pd.read_html(url, header=1, flavor='bs4')[0]
        except:
            print('Attempt {}'.format(attempt + 1))
            time.sleep(10)
            continue
        break
    cols = tmp.columns.tolist()
    for i in cols:
        tmp.rename(columns={i:tmp[i][0]},inplace=True)
    tmp.drop(index=0,inplace=True)
    tmp.reset_index(inplace=True,drop=True)
    tmp['Date'] = tgt_dt
    tmp['ObsTime'] = tmp['ObsTime'].apply(int)
    df = df.append(tmp)
    tgt_dt += relativedelta(months=1)


null_idx = df.loc[df['Temperature']=='...'].index.tolist()
df.at[null_idx,'Temperature'] = '-3'

### Filling / in StnPres,Temperature,RH,WS,WD
error_idx = pd.Series(df.loc[df['Temperature']=='/'].index)
prev_values = df.loc[list(error_idx-1),'Temperature'].reset_index()
while not(prev_values[prev_values['Temperature'] == '/'].empty):
    prev_values = prev_values.apply(lambda x: x['index']-1 if x['Temperature']=='/' else x,axis=1).drop(columns=['Temperature'])
    prev_values['Temperature'] = prev_values['index'].apply(lambda x: df.loc[x,'Temperature'])
next_values = df.loc[list(error_idx+1),'Temperature'].reset_index()
while not(next_values[next_values['Temperature'] == '/'].empty):
    next_values = next_values.apply(lambda x: x['index']+1 if x['Temperature']=='/' else x,axis=1).drop(columns=['Temperature'])
    next_values['Temperature'] = next_values['index'].apply(lambda x: df.loc[x,'Temperature'])
next_values_ls = next_values['Temperature'].values.tolist()
prev_values_ls = prev_values['Temperature'].values.tolist()
for i in range(len(error_idx)):
    temp_avg = (eval(prev_values_ls[i])+eval(next_values_ls[i]))/2
    df.at[error_idx.values.tolist()[i],'Temperature'] = str(round(temp_avg,1))

### Convert to int and floats
df['Temperature'] = df['Temperature'].apply(eval)
n3_idx = df.loc[(df['Temperature']==-3) | (df['Temperature']==-3.0)].index.tolist()
df.at[n3_idx,'Temperature'] = np.nan
df['Date'] = pd.to_datetime(df['Date'])
df = df[['Date','ObsTime','StnPres', 'SeaPres', 'Temperature', 'RH', \
       'WS', 'WD', 'WSGust', 'WDGust', 'Precp', 'PrecpHour', 'SunShine', \
       'GloblRad', 'Visb', 'UVI']]

