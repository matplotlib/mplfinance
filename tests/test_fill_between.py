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



def test_fill_between06(bolldata):

    #df = _get_data_subset(bolldata)
    df = bolldata
    fname,tname,rname = _get_file_names('06')

    # =======
    #  MACD:
    
    exp12     = df['Close'].ewm(span=12, adjust=False).mean()
    exp26     = df['Close'].ewm(span=26, adjust=False).mean()
    macd      = exp12 - exp26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    
    fb_12up = dict(y1=exp12.values,y2=exp26.values,where=(exp12>exp26).values,color="#93c47d",alpha=0.6,interpolate=True)
    fb_12dn = dict(y1=exp12.values,y2=exp26.values,where=(exp12<exp26).values,color="#e06666",alpha=0.6,interpolate=True)
    fb_exp12 = [fb_12up,fb_12dn]
    
    fb_macd_up = dict(y1=macd.values,y2=signal.values,where=(signal<macd).values,color="#93c47d",alpha=0.6,interpolate=True)
    fb_macd_dn = dict(y1=macd.values,y2=signal.values,where=(signal>macd).values,color="#e06666",alpha=0.6,interpolate=True)
    
    fb_macd = [fb_macd_up,fb_macd_dn]
    
    s = mpf.make_mpf_style(base_mpf_style='blueskies',facecolor='aliceblue')

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    for tag in ['a','b','c']:
        apds = [mpf.make_addplot(exp12,color='lime'),
                mpf.make_addplot(exp26,color='c'),
                mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                                 color='dimgray',alpha=0.65,secondary_y=True),
                mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=False),
                mpf.make_addplot(signal,panel=1,color='b',secondary_y=False)
               ]

        new_tname = tname[0:-4]+tag+tname[-4:]
        if tag == 'a':
            print('fb_exp12')
            pp.pprint(fb_exp12)
            print('fb_macd')
            pp.pprint(fb_macd)
            apds[ 0] = mpf.make_addplot(exp12,color='lime',fill_between=fb_exp12)
            apds[-1] = mpf.make_addplot(signal,panel=1,color='b',secondary_y=False,fill_between=fb_macd)
            mpf.plot(df,type='candle',addplot=apds,figscale=0.8,figratio=(1,1),title='\n\nMACD',
                     style=s,volume=True,volume_panel=2,panel_ratios=(3,4,1),tight_layout=True,
                     savefig=new_tname)
        elif tag == 'b':
            print('fb_exp12')
            pp.pprint(fb_exp12)
            print('fb_macd')
            pp.pprint(fb_macd)
            apds[ 0] = mpf.make_addplot(exp12,color='lime')
            apds[-1] = mpf.make_addplot(signal,panel=1,color='b',secondary_y=False,fill_between=fb_macd)
            mpf.plot(df,type='candle',addplot=apds,figscale=0.8,figratio=(1,1),title='\n\nMACD',
                     style=s,volume=True,volume_panel=2,panel_ratios=(3,4,1),tight_layout=True,
                     fill_between=fb_exp12,
                     savefig=new_tname)
        elif tag == 'c':
            apds[ 0] = mpf.make_addplot(exp12,color='lime')
            apds[-1] = mpf.make_addplot(signal,panel=1,color='b',secondary_y=False)
            fb_macd[0]['panel'] = 1
            fb_macd[1]['panel'] = 1
            print('fb_exp12')
            pp.pprint(fb_exp12)
            print('fb_macd')
            pp.pprint(fb_macd)
            print('fb_macd+fb_exp12')
            pp.pprint(fb_macd+fb_exp12)
            mpf.plot(df,type='candle',addplot=apds,figscale=0.8,figratio=(1,1),title='\n\nMACD',
                     style=s,volume=True,volume_panel=2,panel_ratios=(3,4,1),tight_layout=True,
                     fill_between=fb_macd+fb_exp12,
                     savefig=new_tname)
        else:
            print('Should NEVER get to here!')
            raise ValueError('Should NEVER get to here!')
    
        _report_file_sizes(new_tname,rname)

        result = compare_images(rname,new_tname,tol=IMGCOMP_TOLERANCE)
        if result is not None:
           print('result=',result)
        assert result is None

