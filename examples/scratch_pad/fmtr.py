####################################################################
#
# https://stackoverflow.com/questions/25777037/how-can-i-left-justify-text-in-a-pandas-dataframe-column-in-an-ipython-notebook
#
####################################################################

import mplfinance as mpf
import pandas as pd
import textwrap

vk = mpf.plotting._valid_plot_kwargs()

df = (pd.DataFrame(vk).T.head(18)).drop('Validator',axis=1)

df['Kwarg'] = df.index.values
df['Default'] = ["'"+d+"'" if isinstance(d,str) else str(d) for d in df['Default']]

df = df[['Kwarg','Default','Description']]
df = df.head(5).append(df.tail(7))

# df.sort_index(inplace=True)

df 

print('===========================')

print(df)

print('===========================')

def make_left_formatter(maxwidth):
    wm3 = maxwidth-3
    w   = maxwidth
    def left_formatter(value):
        if not isinstance(value,str):
            return f'{value:<}'
        elif value[0:maxwidth] == '-'*maxwidth:
            return f'{value:<{w}.{w}s}'
        #elif len(value) > maxwidth and value[0:maxwidth] != '-'*maxwidth:
        elif len(value) > maxwidth:
            return f'{value:<{wm3}.{wm3}s}...'
        else:
            return f'{value:<{w}.{w}s}'
    return left_formatter

def df_wrapcols(df,wrap_columns=None):

    if wrap_columns is None: return df
    if not isinstance(wrap_columns,dict):
        raise TypeError('wrap_columns must be a dict of column_names and wrap_lengths')

    for col in wrap_columns:
        if col not in df.columns:
            raise ValueError('column "'+str(col)+'" not found in df.columns')

    index = []
    column_data = {}
    for col in df.columns:
        column_data[col] = []
  
    for ix in df.index:
        row = df.loc[ix,]
        
        row_data = {}
        for col in row.index:
            cstr = str(row[col])
            if col in wrap_columns:
                wlen = wrap_columns[col]
                tw   = textwrap.wrap(cstr,wlen) if not cstr.isspace() else [' ']
            else:
                tw = [cstr]
            row_data[col] = tw

        cmax = max(row_data,key=lambda k: len(row_data[k]))
        rlen = len(row_data[cmax])
        for r in range(rlen):
            for col in row.index:
                extension = [' ']*(rlen - len(row_data[col]))
                row_data[col].extend(extension)
                column_data[col].append(row_data[col][r])
            ixstr = str(ix)+'.'+str(r) if r > 0 else str(ix)
            index.append(ixstr)

    return pd.DataFrame(column_data,index=index)

WRAPLEN = 55

df = df_wrapcols(df,wrap_columns={'Description':WRAPLEN})
print('===========================')
print('dfnew1=',df)


# print('===========================')
# df.columns = [ ' '+col for col in df.columns ]

dividers = []
for col in df.columns:
    dividers.append('-'*int(df[col].str.len().max()))
dfd = pd.DataFrame(dividers).T
dfd.columns = df.columns
dfd.index = pd.Index(['---'])

print('===========================')

df = dfd.append(df)

fmts = {'Kwarg': make_left_formatter(df['Kwarg'].str.len().max()+1),
        'Description': make_left_formatter(WRAPLEN),
        'Default': make_left_formatter(8),
       }
s = df.to_string(formatters=fmts,index=False,justify='left')

print('\n ',s.replace('\n','\n  '))

print('===========================')

