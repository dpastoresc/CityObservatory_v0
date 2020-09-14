#-------------------------------------------------------------------------------------------
'''
#barchar and histogram of sensors
df = pd.read_csv('../data/trafico/raw_data/07-2020.csv', sep=';')

df_month = df.groupby(['id']).mean()

fig = px.bar(x = df_month.index, y=df_month['intensidad'])
fig.show()

fig = px.histogram(df_month, x = 'intensidad', nbins=50)
fig.show()

#output sensors by day to cluster them
#not needed
df_pivot = df.pivot(index='id', columns='fecha', values='intensidad')

df_pivot.to_csv('out/total.csv')

np.save('out/total.npy', df_pivot.to_numpy())

for i in range(1,32):
    dates = [str(x) for x in pd.date_range(start = '7/' + str(i) +'/2020', periods=24*4, freq='15min').tolist()]
    df_slice = df_pivot[dates]
    df_slice.to_csv('out/7-' + str(i) +'-2020.csv')
    np.save('out/7-' + str(i) +'-2020.npy', df_slice.to_numpy())
    print(i)
print('finished')

#####------------------------Datos de COVID por Zonas Básicas de Salud-----------------------------------------

'''

import pandas as pd
import os
from utils import getRootPath
import json

'''
filepath = os.path.join(getRootPath(), 'data/bike/raw_data/202001_movements.json')

f = open(filepath)
filepath_output = filepath[:filepath.rfind('.json')] + '_out.json'
f_out = open(filepath_output, "w+")
Lines = f.readlines()
f_out.write('[')
last_line = None
for line in Lines:
    print(line.strip())
    if not last_line == None:
        f_out.write(line.strip() +',')
    last_line = line
f_out.write(']')
'''
print('fin')
