#!/bin/env python

import pandas     as pd
import mplfinance as mpf

Dates  = ['2019-11-06', '2019-11-07', '2019-11-08', '2019-11-11', '2019-11-12']
Open   = [3075.1, 3092.0, 3092.0, 3080.33, 3089.28]
High   = [3078.34, 3096.0, 3096.0, 3088.33, 3102.61]
Low    = [3065.89, 3081.0, 3081.0, 3075.82, 3084.73]
Close  = [3076.78, 3085.0, 3085.0, 3087.01, 3091.84]
Volume = [544288522, 566117910, 460757054, 366044400, 434953689]

data = dict(Open=Open,High=High,Low=Low,Close=Close,Volume=Volume)
df   = pd.DataFrame(data,index=pd.DatetimeIndex(Dates))

df.loc['2019-11-07','Open' ] = 3085
df.loc['2019-11-07','Close'] = 3092
df.loc['2019-11-07','Low'  ] = 3081
df.loc['2019-11-07','High' ] = 3096

df.loc['2019-11-08','Open' ] = 3085
df.loc['2019-11-08','Close'] = 3092
df.loc['2019-11-08','Low'  ] = 3081
df.loc['2019-11-08','High' ] = 3096


dfs = df.copy()
dfs.loc['2019-11-07','Open' ] = 3092
dfs.loc['2019-11-07','Close'] = 3085

dfs.loc['2019-11-08','Open' ] = 3092
dfs.loc['2019-11-08','Close'] = 3085

df  = df.iloc[0:3]
dfs = dfs.iloc[0:3]

kwargs=dict(type='hollow_candle',figratio=(8,10),figscale=2.0,update_width_config=dict(candle_linewidth=4.25))


# s = mpf.make_mpf_style(base_mpf_style='charles',gridstyle='',facecolor='#79c0c3')
# s = mpf.make_mpf_style(base_mpf_style='charles',gridstyle='',facecolor='gainsboro')
# s = mpf.make_mpf_style(base_mpf_style='charles',gridstyle='',facecolor='pink')
# s = mpf.make_mpf_style(base_mpf_style='charles',gridstyle='',facecolor='#ffd6dd')
s = mpf.make_mpf_style(base_mpf_style='charles',gridstyle='')

mpf.plot(df ,style=s,**kwargs,savefig='hollow_red_green.jpg')
mpf.plot(dfs,style=s,**kwargs,savefig='solid_red_green.jpg')

# st1 = mpf.make_mpf_style(base_mpf_style='checkers',gridstyle='',facecolor='#56b0b3')
mc = mpf.make_marketcolors(base_mpf_style='checkers',down='#a02128')
st1 = mpf.make_mpf_style(base_mpf_style='checkers',gridstyle='',facecolor='#79c0c3',marketcolors=mc)

mpf.plot(df ,style=st1,**kwargs,savefig='hollow_red_blackt.jpg')
mpf.plot(dfs,style=st1,**kwargs,savefig='solid_red_blackt.jpg')

st2 = mpf.make_mpf_style(base_mpf_style='checkers',gridstyle='',marketcolors=mc)

mpf.plot(df ,style=st2,**kwargs,savefig='hollow_red_black.jpg')
mpf.plot(dfs,style=st2,**kwargs,savefig='solid_red_black.jpg')

st3 = mpf.make_mpf_style(base_mpf_style='classic',gridstyle='',facecolor='#79c0c3')
mpf.plot(df ,style=st3,**kwargs,savefig='hollow_black_white.jpg')
mpf.plot(dfs,style=st3,**kwargs,savefig='solid_black_white.jpg')

##  
##  df = pd.read_csv('data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)
##  
##  df.loc['2019-11-07','Open' ] = 3085
##  df.loc['2019-11-07','Close'] = 3092
##  df.loc['2019-11-07','Low'  ] = 3081
##  df.loc['2019-11-07','High' ] = 3096
##  
##  df.loc['2019-11-08','Open' ] = 3085
##  df.loc['2019-11-08','Close'] = 3092
##  df.loc['2019-11-08','Low'  ] = 3081
##  df.loc['2019-11-08','High' ] = 3096
##  
##  
##  dfs = df.copy()
##  dfs.loc['2019-11-07','Open' ] = 3092
##  dfs.loc['2019-11-07','Close'] = 3085
##  
##  dfs.loc['2019-11-08','Open' ] = 3092
##  dfs.loc['2019-11-08','Close'] = 3085
##  
##  neoclassic = mpf.make_mpf_style(base_mpf_style='classic',facecolor='cyan') 
##  st = neoclassic
##  st = mpf.make_mpf_style(base_mpf_style='nightclouds',gridstyle='')
##  #st = mpf.make_mpf_style(base_mpf_style='sas',gridstyle='') #figcolor='#3C8284'
##  st1 = mpf.make_mpf_style(base_mpf_style='classic',gridstyle='',facecolor='#56b0b3')
##  #st1 = mpf.make_mpf_style(base_mpf_style='classic',gridstyle='',facecolor='#ffd6dd')
##  mpf.plot(df.iloc[3:8],type='hollow_candle',volume=False,style=st1,figscale=1,update_width_config=dict(candle_linewidth=2.25))
##  mpf.plot(dfs.iloc[3:8],type='hollow_candle',volume=False,style=st1,figscale=1,update_width_config=dict(candle_linewidth=2.25))
##  
