from numbers import Number

import pandas as pd
from pandas.io.stata import StataReader
import numpy as np

pd.set_option('expand_frame_repr', False)

class hhkit(pd.DataFrame):

	# def __init__(self, *args, **kwargs):
	#	pass
		#self.variable_labels = {}
		#self.value_labels = {}
		#self.df = None
		#pd.DataFrame.__init__(self, *args, **kwargs)

	def _is_numeric(self, obj): 
		for element in obj:
			try: 
				0+element
			except TypeError:
				return False
		return True

	def _create_key(self, dfon):
		new_list = []
		for mytuple in zip(*dfon):
			temp_new_list_item = ''
			for item in mytuple:
				temp_new_list_item += str(item)
			new_list += [temp_new_list_item]
		return new_list

	def _initialize_variable_labels(self):
		# make sure variable_labels exists
		try: self.variable_labels
		except: self.variable_labels = {}
		# make sure each column has a variable label
		for var in self.df.columns.values:
			# check if var is already in the list of variable labels
			if var not in self.variable_labels:
				self.variable_labels[var] = ''
		return self.variable_labels

	def set_variable_labels(self, varlabeldict={}):
		self._initialize_variable_labels()
		for var in varlabeldict:
			self.variable_labels[var] = varlabeldict[var]
		return self.variable_labels

	# Here is a 'count' method for calculating household size
	def egen(self, obj, operation, groupby, col, column_label='', include=None, exclude=None, varlabel=''):
		using_excl = False
		df=obj.df
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
		if (self._is_numeric(include)):
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
		self.set_variable_labels(varlabeldict={column_label:varlabel,})
		return merged

	def read_stata(self, *args, **kwargs):
		reader = StataReader(*args, **kwargs)
		self.df = reader.data()
		self.variable_labels = reader.variable_labels()
		self._initialize_variable_labels()
		self.value_labels = reader.value_labels()
		# self.data_label = reader.data_label()
		return self.df

	def sdesc(self, varlist=None, varnamewidth=20, vartypewidth=10, varlabelwidth=70, borderwidthinchars=100):
		if varlist is None:
			list_of_vars = self.df.columns.values
		else:
			list_of_vars = varlist
		print('-'*borderwidthinchars)
		print('obs: %d' % self.df.shape[0])
		print('vars: %d' % len(list_of_vars))
		print('-'*borderwidthinchars)
		# print('--------'.ljust(varnamewidth), '---------'.ljust(vartypewidth), ' ', '--------------'.ljust(varlabelwidth), end='\n')
		print('Variable'.ljust(varnamewidth), 'Data Type'.ljust(vartypewidth), ' ', 'Variable Label'.ljust(varlabelwidth), end='\n')
		print('-'*borderwidthinchars)
		# print('--------'.ljust(varnamewidth), '---------'.ljust(vartypewidth), ' ', '--------------'.ljust(varlabelwidth), end='\n')
		for x in list_of_vars:
			print(repr(x).ljust(varnamewidth), str(self.df[x].dtype).ljust(vartypewidth), ' ', self.variable_labels[x].ljust(varlabelwidth), end='\n')
	
	def from_dict(self, *args, **kwargs):
		self.df = pd.DataFrame(*args, **kwargs)
		self.variable_labels = {}
		self.value_labels = {}
		return self.df

	def statamerge(self, obj, on, how='outer', mergevarname='_m', replacelabels=True):
		df_using_right = obj.df

		# create a unique key based on the 'on' list
		dfon_left_master = [self.df[x] for x in on] 
		dfon_left_master2 = []
		for dfx in dfon_left_master:
			if dfx.dtype is not np.dtype('object'): # We want to allow string keys
				dfon_left_master2 += [dfx.astype(float)] # We want 1 and 1.0 to be considered equal when converted
														 # 	to a string, so make them 1.0 and 1.0 respectively
			else:
				dfon_left_master2 += [dfx]
		dfon_right_using = [df_using_right[x] for x in on]
		dfon_right_using2 = []
		for dfx in dfon_right_using:
			if dfx.dtype is not np.dtype('object'):
				dfon_right_using2 += [dfx.astype(float)]
			else:
				dfon_left_master2 += [dfx]		
		left_master_on_key = self._create_key(dfon_left_master2)
		right_using_on_key = self._create_key(dfon_right_using2)

		# create a new column in each dataset with the combined key
		self.df['_left_merge_key'] = pd.Series(left_master_on_key)
		df_using_right['_right_merge_key'] = pd.Series(right_using_on_key)
		self.df = pd.merge(self.df, df_using_right, on=on, how=how)
		self.df[mergevarname] = 0
		self.df[mergevarname][self.df['_left_merge_key'].isnull()] = 2
		self.df[mergevarname][self.df['_right_merge_key'].isnull()] = 1
		self.df[mergevarname][self.df[mergevarname] == 0 ] = 3
		del self.df['_left_merge_key']
		del self.df['_right_merge_key']

		# How about the variable labels?
		variable_labels_to_add_to_merged_dataset_dict = {}
		try: 
			obj.variable_labels
		except: 
			obj.variable_labels = {}
		if (replacelabels): # replace the variable lables with those in the right/using dataset
			for var in obj.variable_labels:
				if (not obj.variable_labels[var]==""):
					variable_labels_to_add_to_merged_dataset_dict[var]=obj.variable_labels[var]
		else: # don't replace the variable lables with those in the right/using dataset, just add variable labels
			  #		for variables that are not already in the left/master dataset
			for var in obj.variable_labels:
				if var not in self.variable_labels:
					variable_labels_to_add_to_merged_dataset_dict[var]=obj.variable_labels[var]
		self.set_variable_labels(variable_labels_to_add_to_merged_dataset_dict)
		self._initialize_variable_labels()

		return self.df

