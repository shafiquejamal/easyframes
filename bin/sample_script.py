import pandas as pd
import numpy as np
from easyframes.easyframes import hhkit

# myhhkit = hhkit('mydataset.dta', encoding="latin-1")

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

hhkm = hhkit(df_master) 
hhkh = hhkit(df_using_hh)  
hhki = hhkit(df_using_ind) 

print(hhkm.df)
print(hhkh.df)
print(hhki.df)

# Egen commands
hhkm.egen(operation='count', groupby='hh', column='hh', column_label='hhsize')
print(hhkm.df)

hhkm.egen(operation='mean', groupby='hh', column='age', column_label='mean age in hh')
print(hhkm.df)

hhkm.egen(operation='count', groupby='hh', column='hh', column_label='hhs_o22', include=hhkm.df['age']>22,
			varlabel="hhsize including only members over 22 years of age")
print(hhkm.df)

# Variable labels
hhkm.set_variable_labels({'hh':'Household ID','id':'Member ID'})
hhkm.sdesc()

# Merge commands
hhkm.statamerge(hhkh, on=['hh'], mergevarname='_merge_hh')
print(hhkm.df)
hhkm.sdesc()

hhki.set_variable_labels({'hh':'--> Household ID', 'empl':'Employment status'})
hhkm.statamerge(hhki, on=['hh','id'], mergevarname='_merge_ind')
print(hhkm.df)
hhkm.sdesc()

# Tabulations
df_tab_m1 = hhkm.tab('_merge_hh', p=True)
df_tab_m2 = hhkm.tab('_merge_ind', p=True)
df_tab = hhkm.tab('educ', p=True)
hhkm.set_variable_labels({'educ':'Level of education', 'house_rooms':'Number of rooms in the house',})
df_tab = hhkm.tab('educ', p=True, weightcolumn='weighthh', include=hhkm.df['age'] > 10, usevarlabels=True)

df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, usevarlabels=[False, False], p=True)
df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, p=True)
df_tab = hhkm.tab(['educ','house_rooms'], decimalplaces=5, usevarlabels=[True, True], 
			p=True, include=hhkm.df['age'] > 10, weightcolumn='weighthh')

# Recode/replace
include = pd.Series([True, False, True, False, True, True, False, True, 
					 True, True, False, True, False, True, False, False, True],
			index=np.arange(17)) 
hhkm.rr('educ',{'pri':'primary','sec':'secondary','hi':'higher education','bach':'bachelor'}, include=include)
hhkm.rr('has_fence', {0:2,1:np.nan,np.nan:-1}, include=include)
hhkm.rr('has_car', {0:1,1:0,np.nan:-9}, include=include)
print(hhkm.df)