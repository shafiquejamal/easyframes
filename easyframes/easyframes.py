from numbers import Number

import pandas as pd
from pandas.io.stata import StataReader
import numpy as np

pd.set_option('expand_frame_repr', False)

class hhkit(pd.DataFrame):

	def is_numeric(self, obj): 
		for element in obj:
			try: 
				0+element
			except TypeError:
				return False
		return True

	# Here is a 'count' method for calculating household size
	def egen(self, df, operation, groupby, col, column_label='', include=None, exclude=None):
		using_excl = False
		if (include is None) and (exclude is None):
			# Make an array or data series same length as df with all entries true - all rows are included
			include = pd.Series([True]*df.shape[0])
		elif (include is not None) and (exclude is not None):
			# raise an error saying that can only specify one
			raise Exception("Specify either include or exclude, but not both")
		elif (include is not None):
			# check that dimensions and content are correct
			pass
		elif (exclude is not None):
			# check that dimensions and content are correct
			using_excl = True
			include = exclude
			# include = np.invert(exclude)

		# Lets make sure we work with boolean include arrays/series. Convert numeric arrays to boolean
		if (self.is_numeric(include)):
			# Make this a boolean
			include = [x!=0 for x in include]
		elif (include.dtype is not np.dtype('bool')):
			raise Exception('The include and exclude series or arrays must be either numeric or boolean.')

		if (using_excl):
			include = np.invert(include)

		if column_label == '':
			column_label = '('+operation+') '+col+' by '+groupby

		result = df[include].groupby(groupby)[col].agg([operation])
		result.rename(columns={operation:column_label}, inplace=True)
		merged = pd.merge(df, result, left_on=groupby, right_index=True, how='left')
		self.df = merged
		return merged

	def read_stata(self, *args, **kwargs):
		reader = StataReader(*args, **kwargs)
		self.df = reader.data()
		self.variable_labels = reader.variable_labels()
		self.value_labels = reader.value_labels()
		# self.data_label = reader.data_label()
		return self.df

	def sdesc(self, varlist=None, varnamewidth=15, vartypewidth=10, varlabelwidth=70):
		if varlist is None:
			list_of_vars = self.df.columns.values
		else:
			list_of_vars = varlist
		print('obs: %d' % self.df.shape[0])
		print('vars: %d' % len(list_of_vars))
		print('--------'.ljust(varnamewidth), '---------'.ljust(vartypewidth), ' ', '--------------'.ljust(varlabelwidth), end='\n')
		print('Variable'.ljust(varnamewidth), 'Data Type'.ljust(vartypewidth), ' ', 'Variable Label'.ljust(varlabelwidth), end='\n')
		print('--------'.ljust(varnamewidth), '---------'.ljust(vartypewidth), ' ', '--------------'.ljust(varlabelwidth), end='\n')
		for x in list_of_vars:
			print(repr(x).ljust(varnamewidth), str(self.df[x].dtype).ljust(vartypewidth), ' ', self.variable_labels[x].ljust(varlabelwidth), end='\n')
	
	def statamerge(self, df_using_right):
		pass
