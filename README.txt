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
from easyframes.easyframes import hhkit

myhhkit = hhkit('sample_hh_dataset.csv')
myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhsize')
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
myhhkit.egen(myhhkit, operation='mean', groupby='hh', col='age', column_label='mean age in hh')
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
myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhs_o22', include=df['age']>22)

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
df = myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhs_o22', 
	exclude=df['age']>22)
```
If you don't specify the column label, then a default is constructed:
```
df = myhhkit.egen(myhhkit, operation='mean', groupby='hh', col='age')
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

What about variable labels? They are supported too:

```
df_master = pd.DataFrame(
	{'educ': {0: 'secondary', 1: 'bachelor', 2: 'primary', 3: 'higher', 4: 'bachelor', 5: 'secondary', 
		6: 'higher', 7: 'higher', 8: 'primary', 9: 'primary'}, 
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
myhhkit.from_dict(df_master)
myhhkit.set_variable_labels({'hh':'Household ID','id':'Member ID'})
print(myhhkit.sdesc())
```
```
-------------------------------------------------------------------------
obs: 10
vars: 10
-------------------------------------------------------------------------
Variable             Data Type    Variable Label                                                        
--------------------------------------------------------------------------
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
```
You can even specify a variable label when using egen:
```
myhhkit = hhkit('sample_hh_dataset.csv')
myhhkit.set_variable_labels({'age':'Age in years'})
myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhs_o22', 
	include=df['age']>22, varlabel='Household size including only members over 22 years of age')
print(myhhkit.df)
print(myhhkit.sdesc())	
```
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
--------------------------------------------------------------------------------
obs: 10
vars: 11
--------------------------------------------------------------------------------
Variable             Data Type    Variable Label                                                        
--------------------------------------------------------------------------------
'id'                 int64                         
'hh'                 int64                                  
'fridge'             object                                  
'age'                int64        Age in years                            
'male'               int64                               
'house_rooms'        int64                                
'has_car'            int64                                    
'weighthh'           int64                             
'prov'               object                                 
'educ'               object                                 
'hhs_o22'            int64        Household size including only members over 22 years of age 
```
There is also a Stata-like merge method, which creates a merge variable for you in the dataset (and copies over the variable labesl):
```
df_master = pd.DataFrame(
	{'educ': {0: 'secondary', 1: 'bachelor', 2: 'primary', 3: 'higher', 4: 'bachelor', 5: 'secondary', 
		6: 'higher', 7: 'higher', 8: 'primary', 9: 'primary'}, 
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
	{'empl': {0: 'not employed', 1: 'full-time', 2: 'part-time', 3: 'part-time', 4: 'full-time', 5: 'part-time', 
		6: 'self-employed', 7: 'full-time', 8: 'self-employed'}, 
	 'hh': {0: 1, 1: 1, 2: 1, 3: 2, 4: 5, 5: 5, 6: 4, 7: 4, 8: 4},  
	 'id': {0: 1, 1: 2, 2: 4, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 5}
     })
myhhkit.from_dict(df_master) # If the object already exists, you can replace the existing dataframe. You 
							 # 	can pass a data frame or a dict to the from_dict() method.
myhhkit.set_variable_labels({'hh':'Household ID','id':'Member ID'})

# Now merge:
myhhkit_using_hh = hhkit(df_using_hh)
myhhkit_using_hh.set_variable_labels({'hh':'--> Household ID','has_fence':'This dwelling has a fence'})
myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh', replacelabels=False) 
print(myhhkit.df)
print(myhhkit.sdesc())
```
```
    age       educ fridge  has_car  hh  house_rooms  id  male     prov  weighthh  has_fence  _merge_hh
0    44  secondary    yes        1   1            3   1     1       BC         2        NaN          1
1    43   bachelor    yes        1   1            3   2     0       BC         2        NaN          1
2    13    primary    yes        1   1            3   3     1       BC         2        NaN          1
3    70     higher     no        1   2            2   1     1  Alberta         3          1          3
4    23   bachelor    yes        0   3            1   1     1       BC         2        NaN          1
5    20  secondary    yes        0   3            1   2     0       BC         2        NaN          1
6    37     higher     no        1   4            3   1     1  Alberta         3          0          3
7    35     higher     no        1   4            3   2     0  Alberta         3          0          3
8     8    primary     no        1   4            3   3     0  Alberta         3          0          3
9    15    primary     no        1   4            3   4     0  Alberta         3          0          3
10  NaN        NaN    NaN      NaN   5          NaN NaN   NaN      NaN       NaN          1          2
11  NaN        NaN    NaN      NaN   6          NaN NaN   NaN      NaN       NaN          1          2
12  NaN        NaN    NaN      NaN   7          NaN NaN   NaN      NaN       NaN          0          2
--------------------------------------------------------------------------
obs: 13
vars: 12
--------------------------------------------------------------------------
Variable             Data Type    Variable Label                                                        
--------------------------------------------------------------------------
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
'has_fence'          float64      This dwelling has a fence                    
'_merge_hh'          int64   
```
Another merge, this one replacing the labels in the original/left/master dataset:
```
myhhkit_using_ind = hhkit(df_using_ind)
myhhkit_using_ind.set_variable_labels({'hh':'--> Household ID', 'empl':'Employment status'})
myhhkit.statamerge(myhhkit_using_ind, on=['hh','id'], mergevarname='_merge_ind')
print(myhhkit.df)
print(myhhkit.sdesc())
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