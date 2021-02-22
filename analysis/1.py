import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_table('data', sep='\s+')
fig, ax = plt.subplots()

for key, grp in df.groupby(['color']):
    ax = grp.plot(ax=ax, kind='line', x='x', y='y', c=key, label=key)

plt.legend(loc='best')
plt.show()