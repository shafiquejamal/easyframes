from numbers import Number
from collections import Iterable
import re

import pandas as pd
from pandas.io.stata import StataReader
import numpy as np

pd.set_option('expand_frame_repr', False)

class hhkit(object):

	def __init__(self, *args, **kwargs):
		# if input data frame is specified as a stata data file or text file
		if len(args) > 0:
			if isinstance(args[0], pd.DataFrame):
				self.from_dict(args[0])
			else:
				compiled_pattern = re.compile(r'\.(?P<extension>.{3})$')
				p = re.search(compiled_pattern,str(args[0]))
				if p is not None:
					if (p.group('extension').lower() == "dta"):
						self.read_stata(*args, **kwargs)
					elif (p.group('extension').lower() == "csv" or p.group('extension').lower() == "txt"):
						self.df = pd.read_csv('sample_hh_dataset.csv')
						self._initialize_variable_labels()
					else:
						pass
						# print('Unrecognized file type: %s' % p.group('extension'))
				else:
					pass
					print('Unrecognized file type: %s' % p.group('extension'))
					

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

	def _make_include_exclude_series(self, df, include, exclude):
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
		if (self._is_numeric(include)):
			# Make this a boolean
			include = [x!=0 for x in include]
		elif (include.dtype is not np.dtype('bool')):
			raise Exception('The include and exclude series or arrays must be either numeric or boolean.')

		if (using_excl):
			include = np.invert(include)
		return include

	def set_variable_labels(self, varlabeldict={}):
		self._initialize_variable_labels()
		for var in varlabeldict:
			self.variable_labels[var] = varlabeldict[var]
		return self.variable_labels

	# Here is a 'count' method for calculating household size
	def egen(self, obj, operation, groupby, col, column_label='', include=None, exclude=None, varlabel=''):
		df=obj.df
		include = self._make_include_exclude_series(df, include, exclude)

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

	def tab(self, columns, shownan=False, p=True, includenan=True, includenanrows=True, 
				includenancols=True, dropna=False, decimalplaces=5, usevarlabels=[True, True],
				include=None, exclude=None):
		
		include = self._make_include_exclude_series(self.df, include, exclude)

		if (isinstance(columns, str) or (isinstance(columns, Iterable) and len(columns)==1)): 
		# One way tabulation - tabulation of one variable
			if (isinstance(columns, str)):
				column = columns
			else:
				column = columns[0]
			self.df['_deleteme'] = 1
			if (includenan):
				table = pd.crosstab(columns=self.df[column][include].astype(str), index=self.df['_deleteme'][include], dropna=dropna)
			else:
				table = pd.crosstab(columns=self.df[column][include], index=self.df['_deleteme'][include], dropna=dropna)
			table1 = pd.DataFrame(table.sum(axis=0))
			table1.index.names = [column]
			table1.columns = ['count']
			table1['percent'] = 100*table1['count']/table1['count'].sum()
			del self.df['_deleteme']
			
			# make sure the 'nan' is at the bottom, if it is there at all
			if ('nan' in table1.index):
				table1 = pd.concat([table1[table1.index != 'nan'], table1[table1.index == 'nan']])

			# use variable labels?
			if (isinstance(usevarlabels, bool)):
				if (usevarlabels == True):
					table1.index.name = self.variable_labels[column]

			# Add a row with totals
			table1.loc['total'] = [table1['count'].sum(), table1['percent'].sum()]

			if (p):
				print(table1)
			return table1
		elif (isinstance(columns, Iterable)):
			if (includenanrows and includenancols):
				table = pd.crosstab(self.df[columns[0]][include].astype(str), self.df[columns[1]][include].astype(str), dropna=dropna)
			elif (includenanrows and not includenancols):
				table = pd.crosstab(self.df[columns[0]].astype(str), self.df[columns[1]], dropna=dropna)
			elif (not includenanrows and includenancols):
				table = pd.crosstab(self.df[columns[0]], self.df[columns[1]].astype(str), dropna=dropna)
			else:
				table = pd.crosstab(self.df[columns[0]], self.df[columns[1]], dropna=dropna)
			# Add a heirarchical index

			table1 = table.copy()
			list_of_columns_values = []
			for c in table.columns.values:
				list_of_columns_values += [c]
			# table1.columns = [['count','count'],[table.columns.values[0],table.columns.values[1]]]
			table1.columns = [['count']*len(list_of_columns_values), list_of_columns_values]

			# Get row total
			table1['count','total'] = 0
			for c in table.columns.values:
				table1['count','total'] += table1.xs(('count',c), axis=1)

			# Get row percentages
			for c in table.columns.values:	
				table1['row percent',c] \
			 	 = 100*table1.xs(('count',c), axis=1) / table1.xs(('count','total'), axis=1)

			table1['row percent','total'] = 0
			for c in table.columns.values:
				table1['row percent','total'] += table1.xs(('row percent',c), axis=1)
			
			# Get column percentages
			for c in table.columns.values:
				if (c != 'nan'):
					table1['column percent',c] = 100*table1.xs(('count',c), axis=1) \
				                             /table1.xs(('count',c), axis=1).sum()
				else:
					table1['column percent',c] = np.nan

			# Get cell percentages
			for c in table.columns.values:
				table1['cell percent',c] = 100*table1.xs(('count',c), axis=1) \
				                             /table1.xs(('count','total'), axis=1).sum()
			
			table1['cell percent','total'] = 0
			for c in table.columns.values:
				table1['cell percent','total'] += table1.xs(('cell percent',c), axis=1)

			# move the nans to the end
			if ('nan' in table1.index):
				table1 = pd.concat([table1[table1.index != 'nan'], table1[table1.index == 'nan']])
			dfs_to_concat = []
			for c_upper in ['count','row percent','column percent','cell percent']:
				for c_lower in table.columns.values:
					if (c_lower != 'nan' and c_lower != 'total'):
						dfs_to_concat += [table1[c_upper, c_lower]]
				if ('nan' in table.columns.values):
					dfs_to_concat += [table1[c_upper, 'nan']]
				
				if (c_upper != 'column percent'):
					dfs_to_concat += [table1[c_upper, 'total']]
			table1 = pd.concat(dfs_to_concat, axis=1)

			# Add sensible column names, and add a row of grand totals at the bottom
			table1.columns.names = ['Statistic',columns[1]]
			entries_for_total_row = []
			for c in table1.columns.values:
				if (c[0] != 'row percent'):
					entries_for_total_row += [table1[c].sum()]
				else:
					entries_for_total_row += [np.nan]
			table1.loc['total'] = entries_for_total_row

			table1['row percent','total'] = table1['row percent','total'].apply(np.round, decimals=decimalplaces)
			table1['cell percent','total'] = table1['cell percent','total'].apply(np.round, decimals=decimalplaces)
			for c in table.columns.values:
				table1['row percent',c] = table1['row percent',c].apply(np.round, decimals=decimalplaces)
				table1['column percent',c] = table1['column percent',c].apply(np.round, decimals=decimalplaces)
				table1['cell percent',c] = table1['cell percent',c].apply(np.round, decimals=decimalplaces)

			# Use variable labels?
			if ((usevarlabels is not None) and (len(usevarlabels)==2)):
				if (usevarlabels[0] == True):
					table1.index.name = self.variable_labels[columns[0]]
				if (usevarlabels[1] == True):
					table1.columns.names = [table1.columns.names[0],self.variable_labels[columns[1]]]
			if (p):
				print(table1)
			return table1

		else:
			return False
