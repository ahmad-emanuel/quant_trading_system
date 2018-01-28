
import pandas as pd

max_minute = 6*60 + 30

for minute in range(30,max_minute,60):
    print(minute)




print(str(3)+','+str(1))
df = pd.DataFrame(columns=['first','second'])

series = pd.Series(index=['first','second'])


series['first'] = 1.111
series.second = 2.2222
series.first = 3.333333

df.loc['1'] = series

print('done')