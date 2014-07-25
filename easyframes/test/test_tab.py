import unittest

import pandas as pd
from pandas.util.testing import assert_series_equal
import numpy as np

from easyframes.easyframes import hhkit

class TestTab(unittest.TestCase):

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
	def test_taboneway_gives_correct_tabulations_for_merge_no_weights_no_nans_hh(self):

		myhhkit = hhkit(self.df_master)
		myhhkit_using_hh = hhkit(self.df_using_hh)
		correct_values_taboneway_of_merge_count = pd.Series([5, 3, 5, 13], index=['1','2','3', 'total']).astype(float)
		correct_values_taboneway_of_merge_percent = pd.Series([100*5/13, 100*3/13, 100*5/13, 100*13/13], index=['1','2','3','total'])
		myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh')
		df_tab = myhhkit.tab('_merge_hh', p=False)

		assert_series_equal(correct_values_taboneway_of_merge_count, df_tab['count'])
		assert_series_equal(correct_values_taboneway_of_merge_percent, df_tab['percent'])

	# @unittest.skip("demonstrating skipping")
	def test_taboneway_gives_correct_tabulations_for_varswithnan_no_weights(self):

		myhhkit = hhkit(self.df_master)
		myhhkit_using_hh = hhkit(self.df_using_hh)
		correct_values_taboneway_of_merge_count = pd.Series([2, 3, 4, 1, 3, 13], 
					index=['bach','hi','pri','sec', 'nan', 'total']).astype(float)
		correct_values_taboneway_of_merge_percent = pd.Series([100*2/13, 100*3/13, 100*4/13, 100*1/13, 100*3/13, 100], 
					index=['bach','hi','pri','sec', 'nan', 'total'])
		myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh')

		myhhkit.set_variable_labels({'educ':'Education level','prov':'Province'})
		df_tab = myhhkit.tab('educ', p=False, usevarlabels=True)
		assert_series_equal(correct_values_taboneway_of_merge_count, df_tab['count'])
		assert_series_equal(correct_values_taboneway_of_merge_percent, df_tab['percent'])

		df_tab = myhhkit.tab(['educ'], p=False)
		assert_series_equal(correct_values_taboneway_of_merge_count, df_tab['count'])
		assert_series_equal(correct_values_taboneway_of_merge_percent, df_tab['percent'])

	#@unittest.skip("demonstrating skipping")
	def test_taboneway_gives_correct_tabulations_for_varswithnan_with_weights(self):

		myhhkit = hhkit(self.df_master)
		myhhkit_using_hh = hhkit(self.df_using_hh)
		correct_values_taboneway_of_merge_count_with_w = pd.Series(
					[1.857143, 4.178571, 4.642857, 0.928571, 1.392857, 13], 
					index=['bach','hi','pri','sec', 'nan', 'total']).astype(float)
		correct_values_taboneway_of_merge_percent_with_w = pd.Series(
					[14.285714, 32.142857, 35.714286, 7.142857, 10.714286, 100], 
					index=['bach','hi','pri','sec', 'nan', 'total'])
		myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh')
		myhhkit.df.loc[myhhkit.df['weighthh'].isnull(), ['weighthh']] = 1

		df_tab = myhhkit.tab(['educ'], p=False, weightcolumn='weighthh') 
		assert_series_equal(correct_values_taboneway_of_merge_count_with_w, df_tab['count'])
		assert_series_equal(correct_values_taboneway_of_merge_percent_with_w, df_tab['percent'])

	# @unittest.skip("demonstrating skipping")
	def test_taboneway_gives_correct_tabulations_for_varswithnan_with_weights_with_include(self):

		myhhkit = hhkit(self.df_master)
		myhhkit_using_hh = hhkit(self.df_using_hh)
		correct_values_taboneway_of_merge_count_with_w = pd.Series(
					[1.6, 3.6, 0.8, 6], 
					index=['bach','hi','pri','total']).astype(float)
		correct_values_taboneway_of_merge_percent_with_w = pd.Series(
					[26.666667, 60, 13.333333, 100], 
					index=['bach','hi','pri','total'])
		myhhkit.statamerge(myhhkit_using_hh, on=['hh'], mergevarname='_merge_hh')
		myhhkit.df.loc[myhhkit.df['weighthh'].isnull(), ['weighthh']] = 1

		df_tab = myhhkit.tab(['educ'], p=False, weightcolumn='weighthh', include=myhhkit.df['age']>20) 
		assert_series_equal(correct_values_taboneway_of_merge_count_with_w, df_tab['count'])
		assert_series_equal(correct_values_taboneway_of_merge_percent_with_w, df_tab['percent'])

	# @unittest.skip("demonstrating skipping")
	def test_tabtwoway_withnans(self):
		
		myhhkit = hhkit(self.df_master)
		myhhkit_using_ind = hhkit(self.df_using_ind)
		cv_alberta  = pd.Series([0, 21.42857, 14.28571, 0, 0, 35.71429], 
			index=['bach','hi','pri','sec','nan','total']).astype(float)
		cv_bc  = pd.Series([14.28571, 0, 14.28571, 7.14286, 0, 35.71429], 
			index=['bach','hi','pri','sec','nan','total']).astype(float)
		cv_nan  = pd.Series([0, 0, 0, 0, 28.57143, 28.57143], 
			index=['bach','hi','pri','sec','nan','total']).astype(float)
		cv_total  = pd.Series([14.28571, 21.42857, 28.57143, 7.14286, 28.57143, 100], 
				index=['bach','hi','pri','sec','nan','total']).astype(float)

		myhhkit.set_variable_labels({'educ':'Education level','prov':'Province'})
		myhhkit.statamerge(myhhkit_using_ind, on=['hh','id'], mergevarname='_merge_ind')

		# df_tab = myhhkit.tab(['educ','prov'], decimalplaces=5, usevarlabels=[True, True], p=True)
		df_tab = myhhkit.tab(['educ','prov'], decimalplaces=5, usevarlabels=[True, True], p=False)

		assert_series_equal(cv_alberta,df_tab['cell percent','Alberta'])
		assert_series_equal(cv_bc,df_tab['cell percent','BC'])
		assert_series_equal(cv_nan,df_tab['cell percent','nan'])
		assert_series_equal(cv_total,df_tab['cell percent','total'])

	# @unittest.skip("demonstrating skipping")
	def test_tabtwoway_withnans_using_include_exclude(self):
		
		myhhkit = hhkit(self.df_master)
		myhhkit_using_ind = hhkit(self.df_using_ind)
		cv_alberta  = pd.Series([0, 50, 0, 50], index=['bach','hi','pri','total']).astype(float)
		cv_bc  = pd.Series([33.33333, 0, 16.66667, 50], index=['bach','hi','pri','total']).astype(float)
		cv_total  = pd.Series([33.33333, 50, 16.66667, 100], 
				index=['bach','hi','pri','total']).astype(float)

		myhhkit.set_variable_labels({'educ':'Education level','prov':'Province'})
		myhhkit.statamerge(myhhkit_using_ind, on=['hh','id'], mergevarname='_merge_ind')

		# df_tab = myhhkit.tab(['educ','prov'], decimalplaces=5, usevarlabels=[True, True], p=True)
		df_tab = myhhkit.tab(['educ','prov'], decimalplaces=5, usevarlabels=[True, True], 
			include=myhhkit.df['age']>20, p=False)

		assert_series_equal(cv_alberta,df_tab['cell percent','Alberta'])
		assert_series_equal(cv_bc,df_tab['cell percent','BC'])
		assert_series_equal(cv_total,df_tab['cell percent','total'])
if __name__ == '__main__':

	unittest.main()



