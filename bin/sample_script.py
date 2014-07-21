import pandas as pd

from easyframes.easyframes import hhkit


df_original = pd.read_csv('sample_hh_dataset.csv')
df = df_original.copy()

myhhkit = hhkit()
df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhsize')
df = myhhkit.egen(df, operation='mean', groupby='hh', col='age', column_label='mean age in hh')
df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhs_o22', include=df['age']>22)
df = myhhkit.egen(df, operation='mean', groupby='hh', col='age')

print(df)