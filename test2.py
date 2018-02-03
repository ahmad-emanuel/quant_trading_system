import pandas as pd

df = pd.read_pickle('global_best_solutions')

# trend = sum(df.position[-2][0])
# non_trend = sum(df.position[-2][1])

i= 0
j= 0
trend = df.ix[str(i)+'.'+str(j),'position'][0]
nontrend = df.ix[str(i)+'.'+str(j), 'position'][1]

a = sum(trend)
b = sum(nontrend)

print('finito')
