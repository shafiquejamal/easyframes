import unittest

import pandas as pd
from pandas.util.testing import assert_series_equal
import numpy as np

from easyframes.easyframes import hhkit

class Testrr(unittest.TestCase):

	def setUp(self):

		"""
		df_original = pd.read_csv('sample_hh_dataset.csv')
		df = df_original.copy()
		print(df.to_dict())
		"""
		self.df_master = pd.DataFrame(
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
		self.df_using_hh = pd.DataFrame(
			{'hh':        {0: 2, 1: 4, 2: 5, 3: 6, 4: 7}, 
			 'has_fence': {0: 1, 1: 0, 2: 1, 3: 1, 4: 0}
			})
		self.df_using_ind = pd.DataFrame(
			{'empl': {0: 'ue', 1: 'ft', 2: 'pt', 3: 'pt', 4: 'ft', 5: 'pt', 
				6: 'se', 7: 'ft', 8: 'se'}, 
			 'hh': {0: 1, 1: 1, 2: 1, 3: 2, 4: 5, 5: 5, 6: 4, 7: 4, 8: 4},  
			 'id': {0: 1, 1: 2, 2: 4, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 5}
             })

	# @unittest.skip("demonstrating skipping")
	def test_rr_replaces_values_correctly(self):

		myhhkit = hhkit(self.df_master)
		myhhkit_using_hh = hhkit(self.df_using_hh)
		myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh')
		
		myhhkit.rr({'BC':0,'Alberta':1,np.nan:-1})
		correct_values = pd.Series([0,0,0,1,0,0,1,1,1,1,-1,-1,-1],index=np.arange(13))
		print(myhhkit.df)
		assert_series_equal(correct_values, myhhkit.df['prov'])

if __name__ == '__main__':

	unittest.main()



