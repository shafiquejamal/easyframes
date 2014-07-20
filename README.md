# EasyFrames

## Summary

This package makes it easier to perform some basic operations using a Pandas dataframe. For example, suppose you have the following dataset:

````
... age       educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh
0   44  secondary    yes        1   1            3   1     1       BC         2   
1   43   bachelor    yes        1   1            3   2     0       BC         2   
2   13    primary    yes        1   1            3   3     1       BC         2   
3   70     higher     no        1   2            2   1     1  Alberta         3   
4   23   bachelor    yes        0   3            1   1     1       BC         2   
5   20  secondary    yes        0   3            1   2     0       BC         2   
6   37     higher     no        1   4            3   1     1  Alberta         3   
7   35     higher     no        1   4            3   2     0  Alberta         3   
8    8    primary     no        1   4            3   3     0  Alberta         3   
9   15    primary     no        1   4            3   4     0  Alberta         3   
```` 

If you are using Stata, and you want to add a column with the household size, the command is simple:

`egen hhsize = count(id), by(hh)`

If you are using Pandas and have the dataset loaded as df, you might have to do something like:

```
result = df[include].groupby('hh')['hh'].agg(['count'])
result.rename(columns={'count':'hh size'}, inplace=True)
merged = pd.merge(df, result, left_on='hh', right_index=True, how='left')
```

Using this package, the command would be:

```
from easyframes import hhkit

myhhkit = hhkit()
df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhsize')
```

and Bob's your uncle:

```
   id  hh fridge  age  male  house_rooms  has_car  weighthh     prov       educ  hhsize
0   1   1    yes   44     1            3        1         2       BC  secondary       3
1   2   1    yes   43     0            3        1         2       BC   bachelor       3
2   3   1    yes   13     1            3        1         2       BC    primary       3
3   1   2     no   70     1            2        1         3  Alberta     higher       1
4   1   3    yes   23     1            1        0         2       BC   bachelor       2
5   2   3    yes   20     0            1        0         2       BC  secondary       2
6   1   4     no   37     1            3        1         3  Alberta     higher       4
7   2   4     no   35     0            3        1         3  Alberta     higher       4
8   3   4     no    8     0            3        1         3  Alberta    primary       4
9   4   4     no   15     0            3        1         3  Alberta    primary       4
```

Ok, so it doesn't save much typing or space, but suppose you want to calculate the average age in the household. Here you would simply add
```
df = myhhkit.egen(df, operation='mean', groupby='hh', col='age', 
    column_label='mean age in hh')
```
and the result:
```
   id  hh fridge  age  male  house_rooms  has_car  weighthh     prov       educ  hhsize  mean age in hh
0   1   1    yes   44     1            3        1         2       BC  secondary       3       33.333333
1   2   1    yes   43     0            3        1         2       BC   bachelor       3       33.333333
2   3   1    yes   13     1            3        1         2       BC    primary       3       33.333333
3   1   2     no   70     1            2        1         3  Alberta     higher       1       70.000000
4   1   3    yes   23     1            1        0         2       BC   bachelor       2       21.500000
5   2   3    yes   20     0            1        0         2       BC  secondary       2       21.500000
6   1   4     no   37     1            3        1         3  Alberta     higher       4       23.750000
7   2   4     no   35     0            3        1         3  Alberta     higher       4       23.750000
8   3   4     no    8     0            3        1         3  Alberta    primary       4       23.750000
9   4   4     no   15     0            3        1         3  Alberta    primary       4       23.750000
```

You can also include or exclude certain rows. For example, suppose we want to include in household size only members over the age of 22:
```
df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhs_o22',     include=df['age']>22)

```
The result:
```
   id  hh fridge  age  male  house_rooms  has_car  weighthh     prov       educ  hhs_o22
0   1   1    yes   44     1            3        1         2       BC  secondary        2
1   2   1    yes   43     0            3        1         2       BC   bachelor        2
2   3   1    yes   13     1            3        1         2       BC    primary        2
3   1   2     no   70     1            2        1         3  Alberta     higher        1
4   1   3    yes   23     1            1        0         2       BC   bachelor        1
5   2   3    yes   20     0            1        0         2       BC  secondary        1
6   1   4     no   37     1            3        1         3  Alberta     higher        2
7   2   4     no   35     0            3        1         3  Alberta     higher        2
8   3   4     no    8     0            3        1         3  Alberta    primary        2
9   4   4     no   15     0            3        1         3  Alberta    primary        2
```
You can also exclude members over 22 years of age:
```
df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhs_o22',     exclude=df['age']>22)
```
If you don't specify the column label, then a default is constructed:
```
df = myhhkit.egen(df, operation='mean', groupby='hh', col='age')
```
```
   id  hh fridge  age  male  house_rooms  has_car  weighthh     prov       educ  (mean) age by hh
0   1   1    yes   44     1            3        1         2       BC  secondary         33.333333
1   2   1    yes   43     0            3        1         2       BC   bachelor         33.333333
2   3   1    yes   13     1            3        1         2       BC    primary         33.333333
3   1   2     no   70     1            2        1         3  Alberta     higher         70.000000
4   1   3    yes   23     1            1        0         2       BC   bachelor         21.500000
5   2   3    yes   20     0            1        0         2       BC  secondary         21.500000
6   1   4     no   37     1            3        1         3  Alberta     higher         23.750000
7   2   4     no   35     0            3        1         3  Alberta     higher         23.750000
8   3   4     no    8     0            3        1         3  Alberta    primary         23.750000
9   4   4     no   15     0            3        1         3  Alberta    primary         23.750000
```