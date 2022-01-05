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

WRAPLEN=55

def df_wrapcol(df,wrap_column=None,wrap_length=None):

    if wrap_column is None: return df
    if wrap_length is None: return df

    index = []
    columns = {}
    for col in df.columns:
        columns[col] = []
    nonwrapcols = [col for col in df.columns if col != wrap_column]

    for ix in df.index:
        row = df.loc[ix,]

        swrap = str(row[wrap_column])
        tw  = textwrap.wrap(swrap,wrap_length) if not swrap.isspace() else [' ']

        columns[wrap_column].append(tw[0])
        index.append(str(ix))
        for col in nonwrapcols:
            columns[col].append(row[col])

        if len(tw) > 1:
            for r in range(1,len(tw)):
                columns[wrap_column].append(tw[r])
                index.append(str(ix)+'.'+str(r))
                for col in nonwrapcols:
                    columns[col].append(' ')

    return pd.DataFrame(columns,index=index)


df = df_wrapcol(df,wrap_column='Description',wrap_length=WRAPLEN)
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

