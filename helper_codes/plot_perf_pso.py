import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


test = pd.read_pickle('global_best_solutions')
test2 = pd.read_pickle('global_best_solutions_1')

x = test.index.values
y = test.sharpe

# for i in range(len(x)):
#     x[i] = x[i].replace(',','.')

plt.plot(x,y)
# plt.plot(y);
# plt.xlabel('Iteration number') # The data we generated is unitless, but don't forget units in general.
# plt.ylabel('Sharpe ratio')
# plt.legend(['X', 'Y']);
plt.show()

print('tamam')