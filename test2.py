
import pandas as pd


print(str(3)+','+str(1))
df = pd.DataFrame(columns=['first','second'])

series = pd.Series(index=['first','second'])


series['first'] = 1.111
series.second = 2.2222
series.first = 3.333333

df.loc['1'] = series

print('done')