import pandas as pd

def readDepth(filename): #
    '''
    Reads depth file produced by WinCadence and returns a Pandas DataFrame 
    containing the data.

    Parameters
    -------------
    filename - str
        name of filename from WinCadence

    Returns
    --------------
    data - Pandas DataFrame
        DataFrame containing depth data
    '''
    #! need a docstring, not clear what this does
    data = pd.read_csv(filename, delim_whitespace=True)
    data['Actual Time'] = data['Cycle'] * data['Time']
    data['Time Window Lower Bound'] = data['Actual Time'] - 1
    data['Time Window Lower Bound'][0] = 0
    data['Time Window Upper Bound'] = data['Actual Time'] + 1
    data['Time Window'] = data[['Time Window Lower Bound','Time Window Upper Bound']].apply(tuple, axis=1)


    #! I would recommend using the pandas.drop method 
    del data['Time Window Lower Bound']
    del data['Time Window Upper Bound']
    return data
