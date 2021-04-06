import pandas as pd
from . import libpysal as lps


def df2dbf(df, dbf_path, my_specs=None):
    '''
    Convert a pandas.DataFrame into a dbf.

    __author__  = "Dani Arribas-Bel <darribas@asu.edu>, Luc Anselin <luc.anselin@asu.edu>, Kanahiro Iguchi"
    ...

    Arguments
    ---------
    df          : DataFrame
                  Pandas dataframe object to be entirely written out to a dbf
    dbf_path    : str
                  Path to the output dbf. It is also returned by the function
    my_specs    : list
                  List with the field_specs to use for each column.
                  Defaults to None and applies the following scheme:
                    * int: ('N', 14, 0) - for all ints
                    * float: ('N', 14, 14) - for all floats
                    * str: ('C', 14, 0) - for string, object and category
                  with all variants for different type sizes

    Note: use of dtypes.name may not be fully robust, but preferred apprach of using
    isinstance seems too clumsy
    '''
    if my_specs:
        specs = my_specs
    else:
        type2spec = {'int': ('N', 20, 0),
                     'int8': ('N', 20, 0),
                     'int16': ('N', 20, 0),
                     'int32': ('N', 20, 0),
                     'int64': ('N', 20, 0),
                     'float': ('N', 36, 15),
                     'float32': ('N', 36, 15),
                     'float64': ('N', 36, 15),
                     'str': ('C', 14, 0),
                     'object': ('C', 14, 0),
                     'category': ('C', 14, 0)
                     }
        types = [df[i].dtypes.name for i in df.columns]
        specs = [type2spec[t] for t in types]
    db = lps.io.open(dbf_path, 'w')
    db.header = list(df.columns)
    db.field_spec = specs
    for i, row in df.T.iteritems():
        db.write(row)
    db.close()
    return dbf_path


def dbf2df(dbf_path, index=None, cols=False, incl_index=False):
    '''
    Read a dbf file as a pandas.DataFrame, optionally selecting the index
    variable and which columns are to be loaded.

    __author__  = "Dani Arribas-Bel <darribas@asu.edu>, Kanahiro Iguchi"
    ...

    Arguments
    ---------
    dbf_path    : str
                  Path to the DBF file to be read
    index       : str
                  Name of the column to be used as the index of the DataFrame
    cols        : list
                  List with the names of the columns to be read into the
                  DataFrame. Defaults to False, which reads the whole dbf
    incl_index  : Boolean
                  If True index is included in the DataFrame as a
                  column too. Defaults to False

    Returns
    -------
    df          : DataFrame
                  pandas.DataFrame object created
    '''
    db = lps.io.open(dbf_path)
    if cols:
        if incl_index:
            cols.append(index)
        vars_to_read = cols
    else:
        vars_to_read = db.header
    data = dict([(var, db.by_col(var)) for var in vars_to_read])
    if index:
        index = db.by_col(index)
        db.close()
        return pd.DataFrame(data, index=index, columns=vars_to_read)
    else:
        db.close()
        return pd.DataFrame(data, columns=vars_to_read)
