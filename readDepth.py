import pandas as pd

data = pd.read_csv('Depth.txt',delim_whitespace=True)
data['Actual Time'] = data['Cycle'] * data['Time']
data['Time Window Lower Bound'] = data['Actual Time'] - 1
data['Time Window Lower Bound'][0] = 0
data['Time Window Upper Bound'] = data['Actual Time'] + 1
data['Time Window'] = data[['Time Window Lower Bound','Time Window Upper Bound']].apply(tuple, axis=1)
del data['Time Window Lower Bound']
del data['Time Window Upper Bound']
