#!/usr/bin/env python
# coding: utf-8
import os
import os.path
import glob
import mplfinance        as mpf
import matplotlib.pyplot as plt
from   matplotlib.testing.compare import compare_images

print('mpf.__version__ =',mpf.__version__)                 # for the record
print("plt.rcParams['backend'] =",plt.rcParams['backend']) # for the record

base='fill_between'
tdir = os.path.join('tests','test_images')
refd = os.path.join('tests','reference_images')

globpattern = os.path.join(tdir,base+'*.png')
oldtestfiles = glob.glob(globpattern)

for fn in oldtestfiles:
    try:
        os.remove(fn)
    except:
        print('Error removing file "'+fn+'"')

# IMGCOMP_TOLERANCE = 7.0  # this works fine for linux
IMGCOMP_TOLERANCE = 11.0  # required for a windows pass. (really 10.25 may do it).

def _get_data_subset(bolldata,scaled_down=False):
    start = int(0.2*len(bolldata))
    end   = 2*start
    df = bolldata.iloc[start:end]
    if not scaled_down:
        return df
    scaled_down_data = df/df['Close'].mean()
    scaled_down_data -= 0.9*scaled_down_data['Low'].min()
    return scaled_down_data

def _get_file_names(id):
    fname = base+id+'.png'
    tname = os.path.join(tdir,fname)
    rname = os.path.join(refd,fname)
    return fname,tname,rname

def _report_file_sizes(tname,rname):
    tsize = os.path.getsize(tname)
    print(glob.glob(tname),'[',tsize,'bytes',']')
    rsize = os.path.getsize(rname)
    print(glob.glob(rname),'[',rsize,'bytes',']')


def test_fill_between01(bolldata):

    scaled_down_data  = _get_data_subset(bolldata,True)
    fname,tname,rname = _get_file_names('01')

    mpf.plot(scaled_down_data,figscale=0.7,
             fill_between=scaled_down_data['Close'].values,
             savefig=tname)

    _report_file_sizes(tname,rname)

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_fill_between02(bolldata):

    scaled_down_data  = _get_data_subset(bolldata,True)
    fname,tname,rname = _get_file_names('02')

    mpf.plot(scaled_down_data,figscale=0.7,
             fill_between={'y1':scaled_down_data['Close'].values,'alpha':0.75},
             savefig=tname)

    _report_file_sizes(tname,rname)

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_fill_between03(bolldata):

    df  = _get_data_subset(bolldata)
    fname,tname,rname = _get_file_names('03')

    mpf.plot(df,figscale=0.7,
             fill_between=dict(y1=df['Close'].mean(),
                               y2=df['Close'].values,
                               alpha=0.67),
             type='candle',style='yahoo',savefig=tname)

    _report_file_sizes(tname,rname)

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None

def test_fill_between04(bolldata):

    df  = _get_data_subset(bolldata)
    fname,tname,rname = _get_file_names('04')

    fb_above=dict(y1=df['Close'].mean(),
                  y2=df['Close'].values,
                  alpha=0.5,
                  color='lime',
                  where=((df['Close'] > df['Close'].mean()).values)
                 )

    fb_below=dict(y1=df['Close'].mean(),
                  y2=df['Close'].values,
                  alpha=0.5,
                  color='magenta',
                  where=((df['Close'] < df['Close'].mean()).values)
                 )

    mpf.plot(df,figscale=0.7,
             fill_between=[fb_above,fb_below],
             type='candle',style='yahoo',savefig=tname)

    _report_file_sizes(tname,rname)

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)

def test_fill_between05(bolldata):

    df = _get_data_subset(bolldata)
    fname,tname,rname = _get_file_names('05')

    mpf.plot(df,figscale=0.7,
             fill_between=dict(y1=df['Low'].values,
                               y2=df['High'].values,
                               alpha=0.33),
             type='candle',style='yahoo',savefig=tname)

    _report_file_sizes(tname,rname)

    result = compare_images(rname,tname,tol=IMGCOMP_TOLERANCE)
    if result is not None:
       print('result=',result)
    assert result is None



##  print('''
##  
##  Use a dict to specify two y values, or two series, (y1 and y2) for `fill_between`:
##  
##  ''')
##  
##  mpf.plot(daily,figscale=0.7,fill_between=dict(y1=3090,y2=3120))
##  mpf.plot(daily,figscale=0.7,fill_between=dict(y1=3100,y2=daily['Close'].values))
##  mpf.plot(daily,figscale=0.7,fill_between=dict(y1=daily['Low'].values,y2=daily['High'].values))
##  
##  print('''
##  
##  Use a dict to specify other attributes (kwargs) for `fill_between`:
##  
##  To demonstrate use of the `where` kwarg to display a holding period,
##  we convert the datetime index into a dataframe, and use that to generate a boolean array:
##  
##  `where_values = pd.notnull(dates_df[ (dates_df>=buy_date) & (dates_df <= sell_date) ])['Date'].values`
##  
##  ''')
##  
##  dates_df     = pd.DataFrame(daily.index)
##  buy_date     = pd.Timestamp('2019-11-06')
##  sell_date    = pd.Timestamp('2019-11-19')
##  
##  where_values = pd.notnull(dates_df[ (dates_df>=buy_date) & (dates_df <= sell_date) ])['Date'].values
##  
##  y1values = daily['Close'].values
##  y2value  = daily['Low'].min()
##  
##  mpf.plot(daily,figscale=0.7,
##           fill_between=dict(y1=y1values,y2=y2value,where=where_values,alpha=0.5,color='g')
##          )
##  
##  print('''
##  
##  Use `panel=` in the `fill_between` dict to place the fill_between on a panel other than panel 0:
##  
##  In this example, we `fill_between` on the volume panel, 
##  filling between the volume and the average volume.
##  
##  ''')
##  
##  mpf.plot(daily,volume=True,panel_ratios=(1.1,1),
##           type='candle',tight_layout=True,figratio=(1,1),
##           fill_between=dict(y1=daily['Volume'].values,
##                             y2=daily['Volume'].mean(),
##                             panel=1,alpha=0.5,color='lime'))
##  
##  print('''
##  
##  There are two ways to do multiple `fill_betweens`:
##  (1) Specify a list of `fill_between` dicts.
##  (2) Specify a fill_between (or list of fill_betweens) for each `mpf.make_addplot()`
##  
##  Here, for example, we specify a `fill_between=` a list of fill between dicts:
##  
##  ''')
##  
##  fb1 = dict(y1=daily['Open'].values  , y2=daily['Close'].values , panel=0, alpha=0.3, color='magenta')
##  fb2 = dict(y1=daily['Volume'].values, y2=daily['Volume'].mean(), panel=1, alpha=0.5, color='lime')
##  
##  mpf.plot(daily,volume=True,panel_ratios=(1.1,1),
##           type='candle',tight_layout=True,figratio=(1,1),
##           fill_between=[fb1,fb2])
##  
##  print('''
##  
##  We can accomplish the same thing by specifying one fill_between in `mpf.plot()`
##  and the other in `mpf.make_addplot()`.   This is useful if we are already using
##  `make_addplot()` to plot some additional data.  
##  
##  NOTE: Since make_addplot() accepts a panel argument, one should NOT specify
##        panel in the fill_between dict used by make_addplot.
##  
##  ''')
##  
##  fb1 = dict(y1=daily['Open'].values  , y2=daily['Close'].values , alpha=0.4, color='magenta')
##  fb2 = dict(y1=daily['Volume'].values, y2=daily['Volume'].mean(), alpha=0.5, color='lime')
##  
##  avol = [daily['Volume'].mean()]*len(daily)
##  
##  ap = mpf.make_addplot(avol,panel=1,fill_between=fb2,color='k',linestyle='-.',width=0.25)
##  
##  mpf.plot(daily,volume=True,panel_ratios=(1.1,1),
##           type='candle',tight_layout=True,figratio=(1,1),
##           fill_between=fb1,addplot=ap)
##  
##  print('''
##  
##  We can specify effectively a "multi-color" fill_between, by breaking it into
##  two separate fill_betweens, with two separate colors, each with a "where" clause to
##  indicate where the fill_between color should and should not appear along the datetime axis.
##  
##  This is useful, for example, if we want to highlight where a given value is 
##  above or below the average value.
##  
##  Notice that when using multiple where clauses like this, it is helpful
##  to set `interpolate=True` in the `fill_between` dict, so that the space 
##  between True values and False values also gets filled.
##  
##  ''')
##  
##  fb_above = dict(y1=daily['Volume'].values, 
##                  y2=daily['Volume'].mean(), 
##                  alpha=0.4, color='lime', 
##                  interpolate=True,
##                  where=(daily['Volume'] > daily['Volume'].mean()).values)
##  
##  fb_below = fb_above.copy()
##  fb_below['color'] = 'magenta'
##  fb_below['where'] = (daily['Volume'] < daily['Volume'].mean()).values
##  
##  avol = [daily['Volume'].mean()]*len(daily)
##  ap = mpf.make_addplot(avol,panel=1,fill_between=[fb_above,fb_below],color='k',linestyle='-.',width=0.25)
##  
##  mpf.plot(daily,volume=True,panel_ratios=(0.8,1),
##           type='candle',tight_layout=True,figratio=(1,1),addplot=ap)
##  
##  print('''
##  
##  Here, as an additional example, we create "multi-color" fill_between for both panels:
##  
##  ''')
##  
##  fbvolume_above = dict(y1=daily['Volume'].values, 
##                  y2=daily['Volume'].mean(), 
##                  alpha=0.4, color='lime', 
##                  interpolate=True,
##                  where=(daily['Volume'] > daily['Volume'].mean()).values)
##  
##  fbvolume_below = fbvolume_above.copy()
##  fbvolume_below['color'] = 'magenta'
##  fbvolume_below['where'] = (daily['Volume'] < daily['Volume'].mean()).values
##  
##  avol = [daily['Volume'].mean()]*len(daily)
##  ap = mpf.make_addplot(avol,panel=1,fill_between=[fbvolume_above,fbvolume_below],color='k',linestyle='-.',width=0.25)
##  
##  fbclose_above = dict(y1=daily['Open'].values  , y2=daily['Close'].values , alpha=0.4, 
##                       interpolate=True,
##                       color='lime',
##                       where=(daily['Close']>daily['Open']).values
##                      )
##  
##  fbclose_below = fbclose_above.copy()
##  fbclose_below['color'] = 'magenta'
##  fbclose_below['where'] = (daily['Close']<daily['Open']).values
##  
##  mpf.plot(daily,volume=True,panel_ratios=(1,1),
##           type='candle',tight_layout=True,figratio=(1,1),
##           fill_between=[fbclose_above,fbclose_below],
##           addplot=ap)
##  
##  print('''
##  
##  Finally, as a more pratical example, we use `fill_between` to color a MACD plot:
##  
##  ''')
##  
##  df = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True).loc['2011-07-01':'2011-12-30',:]
##  
##  # =======
##  #  MACD:
##  
##  exp12     = df['Close'].ewm(span=12, adjust=False).mean()
##  exp26     = df['Close'].ewm(span=26, adjust=False).mean()
##  macd      = exp12 - exp26
##  signal    = macd.ewm(span=9, adjust=False).mean()
##  histogram = macd - signal
##  
##  fb_green = dict(y1=macd.values,y2=signal.values,where=signal<macd,color="#93c47d",alpha=0.6,interpolate=True)
##  fb_red   = dict(y1=macd.values,y2=signal.values,where=signal>macd,color="#e06666",alpha=0.6,interpolate=True)
##  fb_green['panel'] = 1
##  fb_red['panel']   = 1
##  fb       = [fb_green,fb_red]
##  
##  apds = [mpf.make_addplot(exp12,color='lime'),
##          mpf.make_addplot(exp26,color='c'),
##          mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
##                           color='dimgray',alpha=1,secondary_y=True),
##          mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=False),
##          mpf.make_addplot(signal,panel=1,color='b',secondary_y=False)#,fill_between=fb),
##         ]
##  
##  s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})
##  
##  mpf.plot(df,type='candle',addplot=apds,figscale=1.6,figratio=(6,5),title='\n\nMACD',
##           style=s,volume=True,volume_panel=2,panel_ratios=(3,4,1),fill_between=fb)
##  
##  def test_fill_between02(bolldata):
