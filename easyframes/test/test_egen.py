import unittest

import pandas as pd
from pandas.util.testing import assert_series_equal
import numpy as np

from easyframes import hhkit

class TestEasyFrames(unittest.TestCase):

	def setUp(self):

		"""
		df_original = pd.read_csv('sample_hh_dataset.csv')
		df = df_original.copy()
		print(df.to_dict())
		"""
		self.df = pd.DataFrame(
			{'educ': {0: 'secondary', 1: 'bachelor', 2: 'primary', 3: 'higher', 4: 'bachelor', 5: 'secondary', 
				6: 'higher', 7: 'higher', 8: 'primary', 9: 'primary'}, 
			 'hh': {0: 1, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 4}, 
			 'has_car': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1}, 
			 'weighthh': {0: 2, 1: 2, 2: 2, 3: 3, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3, 9: 3}, 
			 'house_rooms': {0: 3, 1: 3, 2: 3, 3: 2, 4: 1, 5: 1, 6: 3, 7: 3, 8: 3, 9: 3}, 
			 'prov': {0: 'BC', 1: 'BC', 2: 'BC', 3: 'Alberta', 4: 'BC', 5: 'BC', 6: 'Alberta', 
			 	7: 'Alberta', 8: 'Alberta', 9: 'Alberta'}, 
			 'id': {0: 1, 1: 2, 2: 3, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 3, 9: 4}, 
			 'age': {0: 44, 1: 43, 2: 13, 3: 70, 4: 23, 5: 20, 6: 37, 7: 35, 8: 8, 9: 15}, 
			 'fridge': {0: 'yes', 1: 'yes', 2: 'yes', 3: 'no', 4: 'yes', 5: 'yes', 6: 'no', 
			 	7: 'no', 8: 'no', 9: 'no'}, 
			 'male': {0: 1, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}})
		self.my_include = np.array([False, False, False, True, True, False, True, True, True, False])
		self.my_include_using_integer = np.array([0, 0, 0, 1, 5, 0, -10, -30, -1, 0])
		self.my_include_using_float   = np.array([0, 0, 0, 1, 10.3, 0, -10, -30, -1, 0])

	def test_reject_both_exclude_and_include(self):
		
		myhhkit = hhkit()
		try:
			df2 = myhhkit.egen(self.df, operation='count', groupby='hh', col='hh', 
				exclude=self.my_include, include=self.my_include)
		except:
			return
		raise Exception("Both include and exclude were allowed")

	def test_no_include_no_exclude_includes_all_rows(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='count', groupby='hh', col='hh')
		correct_values = pd.Series([3, 3, 3, 1, 2, 2, 4, 4, 4, 4])
		assert_series_equal(correct_values, df2['(count) hh by hh'])
				
	def test_specify_include_yields_correct_results_count(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='count', groupby='hh', col='hh', include=self.my_include)
		correct_values = pd.Series([np.nan, np.nan, np.nan, 1, 1, 1, 3, 3, 3, 3])
		assert_series_equal(correct_values, df2['(count) hh by hh'])

	def test_specify_include_yields_correct_results_mean(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='mean', groupby='hh', col='age', include=self.my_include)
		correct_values = pd.Series([np.nan, np.nan, np.nan, 70, 23, 23, 26.666666, 26.666666, 
																		26.666666, 26.666666])
		assert_series_equal(correct_values, df2['(mean) age by hh'])

	def test_specify_exclude_yields_correct_results_count(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='count', groupby='hh', col='hh', exclude=self.my_include)
		correct_values = pd.Series([3, 3, 3, np.nan, 1, 1, 1, 1, 1, 1])
		assert_series_equal(correct_values, df2['(count) hh by hh'])

	def test_specify_exclude_yields_correct_results_mean(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='mean', groupby='hh', col='age', exclude=self.my_include)
		correct_values = pd.Series([33.333333, 33.333333, 33.333333, np.nan, 20, 20, 15, 15, 15, 15])
		assert_series_equal(correct_values, df2['(mean) age by hh'])

	def test_using_numeric_exclude_type(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='mean', groupby='hh', col='age', exclude=self.my_include_using_integer)
		correct_values = pd.Series([33.333333, 33.333333, 33.333333, np.nan, 20, 20, 15, 15, 15, 15])
		assert_series_equal(correct_values, df2['(mean) age by hh'])

	def test_using_float_exclude_type(self):
		myhhkit = hhkit()
		df2 = myhhkit.egen(self.df, operation='mean', groupby='hh', col='age', exclude=self.my_include_using_float)
		correct_values = pd.Series([33.333333, 33.333333, 33.333333, np.nan, 20, 20, 15, 15, 15, 15])
		assert_series_equal(correct_values, df2['(mean) age by hh'])

if __name__ == '__main__':

	df_original = pd.read_csv('sample_hh_dataset.csv')
	df = df_original.copy()
	myhhkit = hhkit()
	# df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhsize')
	# df = myhhkit.egen(df, operation='mean', groupby='hh', col='age', column_label='mean age in hh')
	# df = myhhkit.egen(df, operation='count', groupby='hh', col='hh', column_label='hhs_o22', include=df['age']>22)
	df = myhhkit.egen(df, operation='mean', groupby='hh', col='age')
	print(df)
	unittest.main()



