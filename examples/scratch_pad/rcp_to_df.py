def rcParams_to_df(rcp,name=None):
    keys = []
    vals = []
    for item in rcp:
        keys.append(item)
        vals.append(rcp[item])
    df = pd.DataFrame(vals,index=pd.Index(keys,name='rcParams Key'))
    if name is not None:
        df.columns = [name]
    else:
        df.columns = ['Value']
    return df
