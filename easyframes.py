import warnings

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)

class hhkit(object):

	def is_numeric_paranoid(self, obj): 
		# https://stackoverflow.com/questions/500328/identifying-numeric-and-array-types-in-numpy
		# Need to turn off warnings for this part - how do I do this?
		try:
			obj+obj, obj-obj, obj*obj, obj**obj, obj/obj
		except ZeroDivisionError:
			return True
		except Exception:
			return False
		else:
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
		if (self.is_numeric_paranoid(include)):
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
		merged['include'] = include
		return merged