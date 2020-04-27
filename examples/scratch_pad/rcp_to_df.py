import pandas as pd


def rcParams_to_df(rcp, name=None):
    keys = []
    vals = []
    for key, value in rcp.items():
        keys.append(key)
        vals.append(value)
    df = pd.DataFrame(vals, index=pd.Index(keys, name='rcParams Key'))
    df.columns = ['Value' if name is None else name]
    return df
