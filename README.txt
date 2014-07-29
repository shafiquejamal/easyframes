# EasyFrames


## Loading datasets

This package makes it easier to perform some basic operations using a Pandas dataframe. For example, suppose you have the following datasets:

```
   age  educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh
0   44   pri    yes        1   1            3   1     1       BC         2
1   43  bach    yes        1   1            3   2     0       BC         2
2   13   pri    yes        1   1            3   3     1       BC         2
3   70    hi     no        1   2            2   1     1  Alberta         3
4   23  bach    yes        0   3            1   1     1       BC         2
5   20   sec    yes        0   3            1   2     0       BC         2
6   37    hi     no        1   4            3   1     1  Alberta         3
7   35    hi     no        1   4            3   2     0  Alberta         3
8    8   pri     no        1   4            3   3     0  Alberta         3
9   15   pri     no        1   4            3   4     0  Alberta         3 
``` 
```
   has_fence  hh
0          1   2
1          0   4
2          1   5
3          1   6
4          0   7
```
```
  empl  hh  id
0   ue   1   1
1   ft   1   2
2   pt   1   4
3   pt   2   1
4   ft   5   1
5   pt   5   2
6   se   4   1
7   ft   4   2
8   se   4   5
```

If you have these datasets already in Stata .dta files, then using easyframes you can load them in like this:
```
myhhkit = hhkit('mydataset.dta', encoding="latin-1")
```
To make this demonstration easy to follow, I will instead load the data from the following Pandas Series from Dicts:
```
df_master = pd.DataFrame(
	{'educ': {0: 'pri', 1: 'bach', 2: 'pri', 3: 'hi', 4: 'bach', 5: 'sec', 
		6: 'hi', 7: 'hi', 8: 'pri', 9: 'pri'}, 
	 'hh': {0: 1, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 4}, 
	 'id': {0: 1, 1: 2, 2: 3, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 3, 9: 4}, 
	 'has_car': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1}, 
	 'weighthh': {0: 2, 1: 2, 2: 2, 3: 3, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3, 9: 3}, 
	 'house_rooms': {0: 3, 1: 3, 2: 3, 3: 2, 4: 1, 5: 1, 6: 3, 7: 3, 8: 3, 9: 3}, 
	 'prov': {0: 'BC', 1: 'BC', 2: 'BC', 3: 'Alberta', 4: 'BC', 5: 'BC', 6: 'Alberta', 
	 	7: 'Alberta', 8: 'Alberta', 9: 'Alberta'}, 
	 'age': {0: 44, 1: 43, 2: 13, 3: 70, 4: 23, 5: 20, 6: 37, 7: 35, 8: 8, 9: 15}, 
	 'fridge': {0: 'yes', 1: 'yes', 2: 'yes', 3: 'no', 4: 'yes', 5: 'yes', 6: 'no', 
	 	7: 'no', 8: 'no', 9: 'no'}, 
	 'male': {0: 1, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}})
df_using_hh = pd.DataFrame(
	{'hh':        {0: 2, 1: 4, 2: 5, 3: 6, 4: 7}, 
	 'has_fence': {0: 1, 1: 0, 2: 1, 3: 1, 4: 0}
	})
df_using_ind = pd.DataFrame(
	{'empl': {0: 'ue', 1: 'ft', 2: 'pt', 3: 'pt', 4: 'ft', 5: 'pt', 
		6: 'se', 7: 'ft', 8: 'se'}, 
	 'hh': {0: 1, 1: 1, 2: 1, 3: 2, 4: 5, 5: 5, 6: 4, 7: 4, 8: 4},  
	 'id': {0: 1, 1: 2, 2: 4, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 5}
     })
```
Here is how you can load the above into easyframes:
```
hhkm = hhkit(df_master) 
hhkh = hhkit(df_using_hh)  
hhki = hhkit(df_using_ind) 

print(hhkm.df)
print(hhkh.df)
print(hhki.df)
```
You can replace the existing dataframe in the hhkit object by passing in a dict or a Pandas DataFrame to the `from_dict` method (even though the method is named `from_dict`, it will still accept a DataFrame object):
```
myhhkit.from_dict(df_master) # If the object already exists, you can replace the existing dataframe. You 
							 # 	can pass a data frame or a dict to the from_dict() method.
```
## Egen commands

If you are using Stata, and you want to add a column with the household size, the command is simple:

`egen hhsize = count(id), by(hh)`

If you are using Pandas and have the dataset loaded as df, and you are NOT using easyframes, then you might have to do something like:

```
result = df[include].groupby('hh')['hh'].agg(['count'])
result.rename(columns={'count':'hh size'}, inplace=True)
merged = pd.merge(df, result, left_on='hh', right_index=True, how='left')
```

Using the easyframes package, the command would be:

```
from easyframes.easyframes import hhkit

hhkm.egen(operation='count', groupby='hh', col='hh', column_label='hhsize')
print(hhkm.df)
```

and Bob's your uncle:

```
   age  educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  hhsize
0   44   pri    yes        1   1            3   1     1       BC         2       3
1   43  bach    yes        1   1            3   2     0       BC         2       3
2   13   pri    yes        1   1            3   3     1       BC         2       3
3   70    hi     no        1   2            2   1     1  Alberta         3       1
4   23  bach    yes        0   3            1   1     1       BC         2       2
5   20   sec    yes        0   3            1   2     0       BC         2       2
6   37    hi     no        1   4            3   1     1  Alberta         3       4
7   35    hi     no        1   4            3   2     0  Alberta         3       4
8    8   pri     no        1   4            3   3     0  Alberta         3       4
9   15   pri     no        1   4            3   4     0  Alberta         3       4
```

Ok, so it doesn't save much typing or space, but suppose you also want to calculate the average age in the household. Here you would simply add the following command
```
hhkm.egen(operation='mean', groupby='hh', col='age', column_label='mean age in hh')
```
and here is the result:
```
   age  educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  hhsize  mean age in hh
0   44   pri    yes        1   1            3   1     1       BC         2       3       33.333333
1   43  bach    yes        1   1            3   2     0       BC         2       3       33.333333
2   13   pri    yes        1   1            3   3     1       BC         2       3       33.333333
3   70    hi     no        1   2            2   1     1  Alberta         3       1       70.000000
4   23  bach    yes        0   3            1   1     1       BC         2       2       21.500000
5   20   sec    yes        0   3            1   2     0       BC         2       2       21.500000
6   37    hi     no        1   4            3   1     1  Alberta         3       4       23.750000
7   35    hi     no        1   4            3   2     0  Alberta         3       4       23.750000
8    8   pri     no        1   4            3   3     0  Alberta         3       4       23.750000
9   15   pri     no        1   4            3   4     0  Alberta         3       4       23.750000
```
You can also include or exclude certain rows. For example, suppose we want to include in household size only members over the age of 22:
```
hhkm.egen(operation='count', groupby='hh', col='hh', column_label='hhs_o22', include=hhkm.df['age']>22,
			varlabel="hhsize including only members over 22 years of age")
print(hhkm.df)
```
The result:
```
   age  educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  hhsize  mean age in hh  hhs_o22
0   44   pri    yes        1   1            3   1     1       BC         2       3       33.333333        2
1   43  bach    yes        1   1            3   2     0       BC         2       3       33.333333        2
2   13   pri    yes        1   1            3   3     1       BC         2       3       33.333333        2
3   70    hi     no        1   2            2   1     1  Alberta         3       1       70.000000        1
4   23  bach    yes        0   3            1   1     1       BC         2       2       21.500000        1
5   20   sec    yes        0   3            1   2     0       BC         2       2       21.500000        1
6   37    hi     no        1   4            3   1     1  Alberta         3       4       23.750000        2
7   35    hi     no        1   4            3   2     0  Alberta         3       4       23.750000        2
8    8   pri     no        1   4            3   3     0  Alberta         3       4       23.750000        2
9   15   pri     no        1   4            3   4     0  Alberta         3       4       23.750000        2
```
You can also exclude members over 22 years of age (just presenting the command, not running it for this demo):
```
hhkm.egen(operation='count', groupby='hh', col='hh', column_label='hhs_o22', exclude=hhkm.df['age']>22,
			varlabel="hhsize including only members over 22 years of age")
```
You'll noticed that I added a variable label. Variable labels are discussed below. If you don't specify the column label, then a default is constructed.

Also, there is an option to sepcify what to replace NaNs with. Egen will fill with NaNs observations where the `col` or `groupby` variables contain NaNs (which can happen after `merge`s, for example.) You can specify `replacenanwith` to replace these NaNs with something else, e.g. `replacenanwith = 0`:

```
hhkm.egen(operation='count', groupby='hh', col='hh', column_label='hhs_o22', exclude=hhkm.df['age']>22,
			varlabel="hhsize including only members over 22 years of age, replacenanwith = 0" )
```

## Variable labels
Variable labels are supported too. 

```
hhkm.set_variable_labels({'hh':'Household ID','id':'Member ID'})
hhkm.sdesc()
```
```
-------------------------------------------------------------------------------------
obs: 10
vars: 13
-------------------------------------------------------------------------------------
Variable             Data Type    Variable Label                                         
-------------------------------------------------------------------------------------
'age'                int64                                                               
'educ'               object                                                              
'fridge'             object                                                              
'has_car'            int64                                                               
'hh'                 int64        Household ID                                           
'house_rooms'        int64                                                               
'id'                 int64        Member ID                                              
'male'               int64                                                               
'prov'               object                                                              
'weighthh'           int64                                                               
'hhsize'             int64                                                               
'mean age in hh'     float64                                                             
'hhs_o22'            int64        hhsize including only members over 22 years of age 
```
## Stata-like Merging

There is also a Stata-like merge method, which creates a merge variable for you in the dataset (and copies over the variable labels):
```
hhkm.statamerge(hhkh, on=['hh'], mergevarname='_merge_hh')
print(hhkm.df)
hhkm.sdesc()
```
```
    age  educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  hhsize  mean age in hh  hhs_o22  has_fence  _merge_hh
0    44   pri    yes        1   1            3   1     1       BC         2       3       33.333333        2        NaN          1
1    43  bach    yes        1   1            3   2     0       BC         2       3       33.333333        2        NaN          1
2    13   pri    yes        1   1            3   3     1       BC         2       3       33.333333        2        NaN          1
3    70    hi     no        1   2            2   1     1  Alberta         3       1       70.000000        1          1          3
4    23  bach    yes        0   3            1   1     1       BC         2       2       21.500000        1        NaN          1
5    20   sec    yes        0   3            1   2     0       BC         2       2       21.500000        1        NaN          1
6    37    hi     no        1   4            3   1     1  Alberta         3       4       23.750000        2          0          3
7    35    hi     no        1   4            3   2     0  Alberta         3       4       23.750000        2          0          3
8     8   pri     no        1   4            3   3     0  Alberta         3       4       23.750000        2          0          3
9    15   pri     no        1   4            3   4     0  Alberta         3       4       23.750000        2          0          3
10  NaN   NaN    NaN      NaN   5          NaN NaN   NaN      NaN       NaN     NaN             NaN      NaN          1          2
11  NaN   NaN    NaN      NaN   6          NaN NaN   NaN      NaN       NaN     NaN             NaN      NaN          1          2
12  NaN   NaN    NaN      NaN   7          NaN NaN   NaN      NaN       NaN     NaN             NaN      NaN          0          2
-------------------------------------------------------------------------------------
obs: 13
vars: 15
-------------------------------------------------------------------------------------
Variable             Data Type    Variable Label                                         
-------------------------------------------------------------------------------------
'age'                float64                                                             
'educ'               object                                                              
'fridge'             object                                                              
'has_car'            float64                                                             
'hh'                 float64      Household ID                                           
'house_rooms'        float64                                                             
'id'                 float64      Member ID                                              
'male'               float64                                                             
'prov'               object                                                              
'weighthh'           float64                                                             
'hhsize'             float64                                                             
'mean age in hh'     float64                                                             
'hhs_o22'            float64      hhsize including only members over 22 years of age     
'has_fence'          float64                                                             
'_merge_hh'          int64 
```
Here is another merge, this one replacing the labels in the original/left/master dataset when the same variable appears in both datasets. I will merge an individual-level dataset with the previously merged dataset:
```
hhki.set_variable_labels({'hh':'--> Household ID', 'empl':'Employment status'})
hhkm.statamerge(hhki, on=['hh','id'], mergevarname='_merge_ind')
print(hhkm.df)
hhkm.sdesc()
```
```
    age       educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  has_fence  _merge_hh           empl  _merge_ind
0    44  secondary    yes        1   1            3   1     1       BC         2        NaN          1   not employed           3
1    43   bachelor    yes        1   1            3   2     0       BC         2        NaN          1      full-time           3
2    13    primary    yes        1   1            3   3     1       BC         2        NaN          1            NaN           1
3    70     higher     no        1   2            2   1     1  Alberta         3          1          3      part-time           3
4    23   bachelor    yes        0   3            1   1     1       BC         2        NaN          1            NaN           1
5    20  secondary    yes        0   3            1   2     0       BC         2        NaN          1            NaN           1
6    37     higher     no        1   4            3   1     1  Alberta         3          0          3  self-employed           3
7    35     higher     no        1   4            3   2     0  Alberta         3          0          3      full-time           3
8     8    primary     no        1   4            3   3     0  Alberta         3          0          3            NaN           1
9    15    primary     no        1   4            3   4     0  Alberta         3          0          3            NaN           1
10  NaN        NaN    NaN      NaN   5          NaN NaN   NaN      NaN       NaN          1          2            NaN           1
11  NaN        NaN    NaN      NaN   6          NaN NaN   NaN      NaN       NaN          1          2            NaN           1
12  NaN        NaN    NaN      NaN   7          NaN NaN   NaN      NaN       NaN          0          2            NaN           1
13  NaN        NaN    NaN      NaN   1          NaN   4   NaN      NaN       NaN        NaN        NaN      part-time           2
14  NaN        NaN    NaN      NaN   5          NaN   1   NaN      NaN       NaN        NaN        NaN      full-time           2
15  NaN        NaN    NaN      NaN   5          NaN   2   NaN      NaN       NaN        NaN        NaN      part-time           2
16  NaN        NaN    NaN      NaN   4          NaN   5   NaN      NaN       NaN        NaN        NaN  self-employed           2
------------------------------------------------------------------------
obs: 17
vars: 14
------------------------------------------------------------------------
Variable             Data Type    Variable Label                                                        
------------------------------------------------------------------------
'age'                float64                    
'educ'               object                            
'fridge'             object                                
'has_car'            float64                           
'hh'                 float64      --> Household ID                             
'house_rooms'        float64                               
'id'                 float64      Member ID                         
'male'               float64                                 
'prov'               object                              
'weighthh'           float64      
'has_fence'          float64      This dwelling has a fence                      
'_merge_hh'          float64                                       
'empl'               object       Employment status                           
'_merge_ind'         int64  
```
The `statamerge` method will not overwrite variables if you set `replacelabels=False` in the method (it is set to `True` by default). After a merge, one normally likes to tabulate the merge variable. That is in the next section. 

## Stata-like tabulations and cross-tabulations (one-way and two-way)

### One-way tabulations

First, lets tabulate a merge variable. This will be a simple one-way tabulation with no weights or exclusions of rows (though we can exclude rows - this is shown further below):
```
df_tab_m1 = hhkm.tab('_merge_hh', p=True)
df_tab_m2 = hhkm.tab('_merge_ind', p=True)
```
```
           count     percent
_merge_hh                   
1.0            5   29.411765
2.0            3   17.647059
3.0            5   29.411765
nan            4   23.529412
total         17  100.000000
            count     percent
_merge_ind                   
1               8   47.058824
2               4   23.529412
3               5   29.411765
total          17  100.000000
```
The `p=True` just means to display the output. Lets do a one-way tabulation of education:
```
df_tab = hhkm.tab('educ', p=True)
```
```
       count     percent
educ                    
bach       2   11.764706
hi         3   17.647059
pri        4   23.529412
sec        1    5.882353
nan        7   41.176471
total     17  100.000000
```
Now lets make it a bit more interesting: lets add weights, exclude some observations, and use the variable label instead of the variable name:
```
hhkm.set_variable_labels({'educ':'Level of education', 'house_rooms':'Number of rooms in the house'})
df_tab = hhkm.tab('educ', p=True, weightcolumn='weighthh', include=hhkm.df['age'] > 10, usevarlabels=True)
```
```
                       count     percent
Level of education                      
bach                1.636364   18.181818
hi                  3.681818   40.909091
pri                 2.863636   31.818182
sec                 0.818182    9.090909
total               9.000000  100.000000
```

### Two-way tabulations

For two-way tabulations, just provide an interable (list or set) of variable names as the first argument:
```
df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, usevarlabels=[False, False], p=True)
```
```
Statistic    count                        row percent                                   column percent                       cell percent                                        
house_rooms    1.0  2.0  3.0  nan  total          1.0       2.0        3.0  nan  total             1.0  2.0        3.0  nan           1.0      2.0       3.0       nan      total
educ                                                                                                                                                                             
bach             1    0    1    0      2           50   0.00000   50.00000    0    100              50    0   14.28571  NaN       5.88235  0.00000   5.88235   0.00000   11.76471
hi               0    1    2    0      3            0  33.33333   66.66667    0    100               0  100   28.57143  NaN       0.00000  5.88235  11.76471   0.00000   17.64706
pri              0    0    4    0      4            0   0.00000  100.00000    0    100               0    0   57.14286  NaN       0.00000  0.00000  23.52941   0.00000   23.52941
sec              1    0    0    0      1          100   0.00000    0.00000    0    100              50    0    0.00000  NaN       5.88235  0.00000   0.00000   0.00000    5.88235
nan              0    0    0    7      7            0   0.00000    0.00000  100    100               0    0    0.00000  NaN       0.00000  0.00000   0.00000  41.17647   41.17647
total            2    1    7    7     17          NaN       NaN        NaN  NaN    NaN             100  100  100.00000  NaN      11.76471  5.88235  41.17647  41.17647  100.00000
```
By default, it will display variable labels instead of variable names:
```
df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, p=True)
```
```
Statistic                     count                        row percent                                   column percent                       cell percent                                        
Number of rooms in the house    1.0  2.0  3.0  nan  total          1.0       2.0        3.0  nan  total             1.0  2.0        3.0  nan           1.0      2.0       3.0       nan      total
Level of education                                                                                                                                                                                
bach                              1    0    1    0      2           50   0.00000   50.00000    0    100              50    0   14.28571  NaN       5.88235  0.00000   5.88235   0.00000   11.76471
hi                                0    1    2    0      3            0  33.33333   66.66667    0    100               0  100   28.57143  NaN       0.00000  5.88235  11.76471   0.00000   17.64706
pri                               0    0    4    0      4            0   0.00000  100.00000    0    100               0    0   57.14286  NaN       0.00000  0.00000  23.52941   0.00000   23.52941
sec                               1    0    0    0      1          100   0.00000    0.00000    0    100              50    0    0.00000  NaN       5.88235  0.00000   0.00000   0.00000    5.88235
nan                               0    0    0    7      7            0   0.00000    0.00000  100    100               0    0    0.00000  NaN       0.00000  0.00000   0.00000  41.17647   41.17647
total                             2    1    7    7     17          NaN       NaN        NaN  NaN    NaN             100  100  100.00000  NaN      11.76471  5.88235  41.17647  41.17647  100.00000
```
Finally, you can do two-way tabulations with weights and excluding selected rows:
```
df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, usevarlabels=[True, True], 
			p=True, include=hhkm.df['age'] > 10, weightcolumn='weighthh')
```
```
Statistic                        count                                row percent                              column percent                  cell percent                               
Number of rooms in the house       1.0       2.0       3.0     total          1.0       2.0        3.0  total             1.0  2.0        3.0           1.0       2.0       3.0      total
Level of education                                                                                                                                                                        
bach                          0.818182  0.000000  0.818182  1.636364           50   0.00000   50.00000    100              50    0   13.33333       9.09091   0.00000   9.09091   18.18182
hi                            0.000000  1.227273  2.454545  3.681818            0  33.33333   66.66667    100               0  100   40.00000       0.00000  13.63636  27.27273   40.90909
pri                           0.000000  0.000000  2.863636  2.863636            0   0.00000  100.00000    100               0    0   46.66667       0.00000   0.00000  31.81818   31.81818
sec                           0.818182  0.000000  0.000000  0.818182          100   0.00000    0.00000    100              50    0    0.00000       9.09091   0.00000   0.00000    9.09091
total                         1.636364  1.227273  6.136364  9.000000          NaN       NaN        NaN    NaN             100  100  100.00000      18.18182  13.63636  68.18182  100.00000
```
There might be more, just have a look at the code (which I need to document better, but hopefully the variable names are helpful). Enjoy!