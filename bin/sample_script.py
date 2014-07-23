import pandas as pd
from easyframes.easyframes import hhkit

# Load a sample dataset, available on the github page for this package
df_original = pd.read_csv('sample_hh_dataset.csv')
df = df_original.copy()
myhhkit = hhkit('sample_hh_dataset.csv')
myhhkit.set_variable_labels({'age':'Age in years'})

# Try some egen commands
print('------------------------------- Some egen commands ---------------------------------')
#myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhsize', varlabel='Household size')
#myhhkit.egen(myhhkit, operation='mean', groupby='hh', col='age', column_label='mean age in hh')
myhhkit.egen(myhhkit, operation='count', groupby='hh', col='hh', column_label='hhs_o22', 
							include=df['age']>22, varlabel='Household size including only members over 22 years of age')
#myhhkit.egen(myhhkit, operation='mean', groupby='hh', col='age')
print(myhhkit.df)
print(myhhkit.sdesc())
print('------------------------------- End some egen commands -----------------------------')

print('------------------------------- Some Stata-like merges ---------------------------------')
# Try some stata-like merges
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

print('---- Left/Master dataset ---')
myhhkit.from_dict(df_master)
myhhkit.set_variable_labels({'hh':'Household ID','id':'Member ID'})
print(myhhkit.df)
print(myhhkit.sdesc())

print('---- Now merging: ---')
myhhkit_using_hh = hhkit(df_using_hh)
# myhhkit_using_hh.from_dict(df_using_hh)
myhhkit_using_hh.set_variable_labels({'hh':'--> Household ID','has_fence':'This dwelling has a fence'})
myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh', replacelabels=False) 
print(myhhkit.df)
print(myhhkit.sdesc())

print('---- Another merge: ---')
myhhkit_using_ind = hhkit(df_using_ind)
# myhhkit_using_ind.from_dict(df_using_ind)
myhhkit_using_ind.set_variable_labels({'hh':'--> Household ID', 'empl':'Employment status'})
myhhkit.statamerge(myhhkit_using_ind, on=['hh','id'], mergevarname='_merge_ind')
print(myhhkit.df)
print(myhhkit.sdesc())
print('------------------------------- End some Stata-like merges ------------------------------')