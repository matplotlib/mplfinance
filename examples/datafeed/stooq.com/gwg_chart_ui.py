"""
ETF Watch

# source: 
    - https://github.com/wgong/watchetf/blob/main/app.py

# app:
    - http://etf.s8s.cloud/
    - https://share.streamlit.io/wgong/watchetf/main/app.py

"""
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
from pathlib import Path
from os.path import join
import re
import pickle
from traceback import format_exc
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import sqlite3

# Initial page config
st.set_page_config(
     page_title=f'GWG_Chart-{datetime.now().strftime("%Y-%m-%d_%H%M")}',
     layout="wide",
     initial_sidebar_state="expanded",
)



@st.experimental_memo
def _load_etf_df():
    WATCH_ETF = """
        #####  watch
        - SPY,SILJ,GDX,AXU,EXK,DBA,WEAT,KHC,TSN,UNG,FCG,XLE,XLB,URA,EWA,XME, tap, argt
        #####  index-sector
        - SPY,QQQ,DIA,IWM,SDS,QID,DXD,XLU,XLRE,XLE,XLB,XME,XLK,XLF,XLV,XLI,XLP,XLY,XLC,UUP, FXE, FXY, BITO
        #####  commodity-agri-metal
        - GSG,DBC,GLD,SLV,GDX,SILJ,COPX,URA,PALL,LIT,DBA,MOO,RJA,CORN,WEAT,COW,JO,WOOD,PHO
        #####  overseas
        - SCHF,SCHC,GWX,EWG,EWQ,EWU,SCZ,ENZL,EWA,EWC,EWW,EWJ,EWY,EWT,IZRL,EIS
        - EFA,MCHI,FXI,KWEB,ASHR,INDA,RSX,EWZ,ARGT,EZA,KSA,TUR
        #####  tech-energy
        - VGT,CLOU,IGV,SMH,USO,BNO,DBO,UNG,BOIL,GRN,ICLN
    """

    # etf_df = pd.read_csv("./data/wl_futures_etf.csv")
    etf_data = [
        {'symbol': 'SPY', 'name': 'S&P 500', 'sector': 'Equity Index', 'order': 0.1} ,
        {'symbol': 'QQQ', 'name': 'Nasdaq 100', 'sector': 'Equity Index', 'order': 0.2} ,
        {'symbol': 'DIA', 'name': 'Dow 30', 'sector': 'Equity Index', 'order': 0.3} ,
        {'symbol': 'IWM', 'name': 'Russell 2000', 'sector': 'Equity Index', 'order': 0.4} ,
        {'symbol': 'SDS', 'name': 'Short S&P 500', 'sector': 'Equity Index', 'order': 0.7} ,
        {'symbol': 'QID', 'name': 'Short Nasdaq 100', 'sector': 'Equity Index', 'order': 0.8} ,
        {'symbol': 'DXD', 'name': 'Short Dow 30', 'sector': 'Equity Index', 'order': 0.9} ,
        {'symbol': 'XLE', 'name': 'Energy', 'sector': 'Sector', 'order': 1.001} ,
        {'symbol': 'XME', 'name': 'Metal', 'sector': 'Sector', 'order': 1.002} ,
        {'symbol': 'XLK', 'name': 'Technology', 'sector': 'Sector', 'order': 1.01} ,
        {'symbol': 'XLF', 'name': 'Financials', 'sector': 'Sector', 'order': 1.02} ,
        {'symbol': 'XLV', 'name': 'Health-care', 'sector': 'Sector', 'order': 1.03} ,
        {'symbol': 'XLI', 'name': 'Industrials', 'sector': 'Sector', 'order': 1.04} ,
        {'symbol': 'XLB', 'name': 'Materials', 'sector': 'Sector', 'order': 1.05} ,
        {'symbol': 'XLP', 'name': 'Consumer Staples', 'sector': 'Sector', 'order': 1.06} ,
        {'symbol': 'XLY', 'name': 'Consumer Discretionary', 'sector': 'Sector', 'order': 1.07} ,
        {'symbol': 'XLC', 'name': 'Communication Services', 'sector': 'Sector', 'order': 1.08} ,
        {'symbol': 'XLU', 'name': 'Utilities', 'sector': 'Sector', 'order': 1.09} ,
        {'symbol': 'XLRE', 'name': 'Real Estate', 'sector': 'Sector', 'order': 1.11} ,
        {'symbol': 'VGT', 'name': 'Vanguard IT', 'sector': 'Technology', 'order': 2.1} ,
        {'symbol': 'CLOU', 'name': 'Global X Cloud Computing', 'sector': 'Technology', 'order': 2.2} ,
        {'symbol': 'IGV', 'name': 'Tech-Software', 'sector': 'Technology', 'order': 2.3} ,
        {'symbol': 'SMH', 'name': 'Semiconductor Index', 'sector': 'Technology', 'order': 2.4} ,
        {'symbol': 'UUP', 'name': 'US Dollar', 'sector': 'Currency', 'order': 3.01} ,
        {'symbol': 'CYB', 'name': 'China Yuan', 'sector': 'Currency', 'order': 3.02} ,
        {'symbol': 'FXE', 'name': 'Euro', 'sector': 'Currency', 'order': 3.03} ,
        {'symbol': 'FXY', 'name': 'Japan Yen', 'sector': 'Currency', 'order': 3.04} ,
        {'symbol': 'UDN', 'name': 'US Dollar - Short', 'sector': 'Currency', 'order': 3.09} ,
        {'symbol': 'BITO', 'name': 'ProShares Bitcoin Strategy', 'sector': 'Currency', 'order': 3.11} ,
        {'symbol': 'USO', 'name': 'United States Oil Fund LP', 'sector': 'Energy', 'order': 4.01} ,
        {'symbol': 'BNO', 'name': 'United States Brent Oil Fund LP', 'sector': 'Energy', 'order': 4.02} ,
        {'symbol': 'DBO', 'name': 'Invesco DB Oil Fund', 'sector': 'Energy', 'order': 4.03} ,
        {'symbol': 'UNG', 'name': 'United States Natural Gas Fund LP', 'sector': 'Energy', 'order': 4.05} ,
        {'symbol': 'BOIL', 'name': 'ProShares Ultra Bloomberg Natural Gas', 'sector': 'Energy', 'order': 4.06} ,
        {'symbol': 'GRN', 'name': 'iPath Series B Carbon ETN', 'sector': 'Energy-Clean', 'order': 4.11} ,
        {'symbol': 'ICLN', 'name': 'iShares Global Clean Energy', 'sector': 'Energy-Clean', 'order': 4.12} ,
        {'symbol': 'GSG', 'name': 'iShares S&P GSCI Commodity-Indexed Trust', 'sector': 'Commodity', 'order': 5.1} ,
        {'symbol': 'DBC', 'name': 'Invesco DB Commodity Index Tracking Fund', 'sector': 'Commodity', 'order': 5.2} ,
        {'symbol': 'GLD', 'name': 'Gold', 'sector': 'Metal', 'order': 6.1} ,
        {'symbol': 'SLV', 'name': 'Silver', 'sector': 'Metal', 'order': 6.2} ,
        {'symbol': 'GDX', 'name': 'Gold miner', 'sector': 'Metal', 'order': 6.3} ,
        {'symbol': 'SILJ', 'name': 'Silver miner', 'sector': 'Metal', 'order': 6.4} ,
        {'symbol': 'COPX', 'name': 'Copper Fund', 'sector': 'Metal', 'order': 6.5} ,
        {'symbol': 'URA', 'name': 'Global X Uranium', 'sector': 'Metal', 'order': 6.6} ,
        {'symbol': 'PALL', 'name': 'Palladium', 'sector': 'Metal', 'order': 6.7} ,
        {'symbol': 'LIT', 'name': 'Global X Lithium & Battery Tech ', 'sector': 'Metal', 'order': 6.8} ,
        {'symbol': 'DBA', 'name': 'Invesco DB Agriculture Fund', 'sector': 'Agri', 'order': 7.01} ,
        {'symbol': 'MOO', 'name': 'VanEck Vectors Agribusiness', 'sector': 'Agri', 'order': 7.02} ,
        {'symbol': 'RJA', 'name': 'Elements Agriculture', 'sector': 'Agri', 'order': 7.03} ,
        {'symbol': 'CORN', 'name': 'Teucrium Corn Fund', 'sector': 'Agri', 'order': 7.05} ,
        {'symbol': 'WEAT', 'name': 'Teucrium Wheat Fund', 'sector': 'Agri', 'order': 7.06} ,
        {'symbol': 'COW', 'name': 'iPath Bloomberg Livestock', 'sector': 'Agri', 'order': 7.07} ,
        {'symbol': 'JO', 'name': 'iPath Bloomberg Coffee Subindex', 'sector': 'Agri', 'order': 7.08} ,
        {'symbol': 'WOOD', 'name': 'iShares Global Timber & Forestry', 'sector': 'Agri', 'order': 7.09} ,
        {'symbol': 'PHO', 'name': 'Invesco Water Resources', 'sector': 'Agri', 'order': 7.11} ,
        {'symbol': 'SCHF', 'name': 'Schwab International Equity', 'sector': 'International', 'order': 10.1} ,
        {'symbol': 'SCHC', 'name': 'Schwab International Small-Cap Equity', 'sector': 'International', 'order': 10.11} ,
        {'symbol': 'GWX', 'name': 'SPDR S&P International Small Cap', 'sector': 'International', 'order': 10.12} ,
        {'symbol': 'EWG', 'name': 'iShares MSCI Germany', 'sector': 'International', 'order': 10.135} ,
        {'symbol': 'EWQ', 'name': 'iShares MSCI France', 'sector': 'International', 'order': 10.1351} ,
        {'symbol': 'EWU', 'name': 'iShares MSCI United Kingdom', 'sector': 'International', 'order': 10.1352} ,
        {'symbol': 'RSX', 'name': 'VanEck Russia', 'sector': 'International', 'order': 10.1353} ,
        {'symbol': 'SCZ', 'name': 'iShares MSCI EAFE Small-Cap', 'sector': 'International', 'order': 10.21} ,
        {'symbol': 'EFA', 'name': 'iShares MSCI EAFE', 'sector': 'International', 'order': 10.22} ,
        {'symbol': 'FXI', 'name': 'iShares China Large-Cap', 'sector': 'International', 'order': 10.23} ,
        {'symbol': 'MCHI', 'name': 'iShares MSCI China', 'sector': 'International', 'order': 10.24} ,
        {'symbol': 'KWEB', 'name': 'KraneShares CSI China Internet', 'sector': 'International', 'order': 10.25} ,
        {'symbol': 'ASHR', 'name': 'Xtrackers Harvest CSI 300 China A-Shares', 'sector': 'International', 'order': 10.26} ,
        {'symbol': 'EWJ', 'name': 'iShares MSCI Japan', 'sector': 'International', 'order': 10.27} ,
        {'symbol': 'EWY', 'name': 'iShares MSCI South Korea', 'sector': 'International', 'order': 10.28} ,
        {'symbol': 'EWT', 'name': 'iShares MSCI Taiwan', 'sector': 'International', 'order': 10.281} ,
        {'symbol': 'INDA', 'name': 'iShares MSCI India', 'sector': 'International', 'order': 10.29} ,
        {'symbol': 'ENZL', 'name': 'iShares MSCI New Zealand', 'sector': 'International', 'order': 10.3} ,
        {'symbol': 'EWA', 'name': 'iShares MSCI-Australia', 'sector': 'International', 'order': 10.31} ,
        {'symbol': 'EWC', 'name': 'iShares MSCI Canada', 'sector': 'International', 'order': 10.4} ,
        {'symbol': 'EWW', 'name': 'iShares MSCI Mexico', 'sector': 'International', 'order': 10.41} ,
        {'symbol': 'EWZ', 'name': 'iShares MSCI Brazil', 'sector': 'International', 'order': 10.42} ,
        {'symbol': 'ARGT', 'name': 'Global X MSCI Argentina', 'sector': 'International', 'order': 10.43} ,
        {'symbol': 'IZRL', 'name': 'ARK Israel Innovative Technology', 'sector': 'International', 'order': 10.6} ,
        {'symbol': 'EIS', 'name': 'iShares MSCI Israel', 'sector': 'International', 'order': 10.61} ,
        {'symbol': 'KSA', 'name': 'iShares MSCI Saudi Arabia', 'sector': 'International', 'order': 10.62} ,
        {'symbol': 'TUR', 'name': 'iShares MSCI Turkey', 'sector': 'International', 'order': 10.63} ,
        {'symbol': 'EZA', 'name': 'iShares MSCI South Africa', 'sector': 'International', 'order': 10.64} ,
    ]
    etf_df = pd.DataFrame.from_dict(etf_data)
    
    # etf_sectors = etf_df["sector"].unique().tolist()
    # manual order
    etf_sectors = ['Equity Index',  'Sector',
        'Currency',  'Commodity',
        'Agri',  'Energy',  'Energy-Clean',
        'Metal',  'Technology',
        'International']

    etf_dict = {}
    for sect in etf_sectors:
        sym_name = etf_df[etf_df["sector"] == sect][["symbol","name"]]
        etf_dict[sect] = dict(zip(sym_name.symbol, sym_name.name))
    
    ticker_name = {}
    for i in etf_data:
        ticker_name[i['symbol']] = i['name']

    return etf_df, etf_sectors, etf_dict, ticker_name, WATCH_ETF

# INITIALIZE settings 
MAX_NUM_TICKERS = 30
NUM_DAYS_QUOTE, NUM_DAYS_PLOT = 390, 250
EMA_FAST, EMA_SLOW, EMA_LONG = 15, 50, 150
EMA_FAST_SCALE, EMA_SLOW_SCALE = 1.4, 2.0 
MA_VOL = 20
RSI_PERIOD, RSI_AVG, RSI_BAND_WIDTH = 100, 25, 0.6
MACD_FAST, MACD_SLOW, MACD_SIGNAL = 12, 26, 9

PANID_PRICE, PANID_VOL, PANID_RSI, PANID_SIGNAL = 0, 3, 2, 1
PANEL_RATIOS = (8, 1, 8, 1)
FIGURE_WIDTH, FIGURE_HEIGHT =  17, 13
YELLOW = '#F5D928'
LIGHT_BLACK = '#8F8E83'

CHART_ROOT = Path.home() / "charts"
if not Path.exists(CHART_ROOT):
    Path.mkdir(CHART_ROOT)
FILE_CACHE_QUOTES = Path.joinpath(CHART_ROOT, "df_quotes_cache.pickle")

DEFAULT_SECTORS = ['Equity Index']
PERIOD_DICT = {"daily":"d", "weekly":"w", "monthly":"m"}
QUOTE_COLUMNS = ["Date", "Ticker", "Chg(%)", "Close", "Low", "High", "Close-1", "Low-1", "High-1"]


FILE_DB = "C:\\gwgllc\\stooq.com\\db_NQ100.sqlite"
# FILE_DB = "C:\\gwgllc\\stooq.com\\db_NASDAQ100_TEST.sqlite"
CHART_TABLE_NAME = "quote_ta"

BACKGROUND_IMG_URL = "https://user-images.githubusercontent.com/329928/155828764-b19a08e4-5346-4567-bba0-0ceeb5c2b241.png"

## i18n strings
_STR_HOME = "home"
_STR_CHART = "chart"
_STR_GWG_CHART = "GWG chart"
_STR_ETF_CHART = "ETF chart"
_STR_REVIEW_CHART = "review chart"
_STR_ETF_DATA = "ETF data"
_STR_APP_NAME = "Mplfinance App"

etf_df, etf_sectors, etf_dict, ticker_name, WATCH_ETF = _load_etf_df()

##############################################
## helper functions
##############################################

@st.cache()
def _query_date_range():
    conn = sqlite3.connect(FILE_DB)
    sql_stmt = f'''
    SELECT min(date_) as begin_date, max(date_) as end_date
    FROM {CHART_TABLE_NAME};
    '''
    df1 = pd.read_sql(sql_stmt, conn)
    return df1.iloc[0][["begin_date", "end_date"]].to_list()

def _make_date_ranges(range_size=NUM_DAYS_PLOT, range_overlap=10):
    """generate date_range windows
    """
    date_range = _query_date_range()
    min_date = pd.to_datetime(date_range[0])
    max_date = pd.to_datetime(date_range[1])
    date_ranges = []
    for i in range(0, (max_date - min_date).days, range_size):
        date_stop = max_date - timedelta(days=i)
        date_start = date_stop - timedelta(days=range_size+range_overlap)
        date_ranges.append((datetime.strftime(date_start,'%Y-%m-%d'), \
                            datetime.strftime(date_stop,'%Y-%m-%d')))
    return date_ranges

@st.cache()
def _query_tickers():
    conn = sqlite3.connect(FILE_DB)
    sql_stmt = f'''
    SELECT distinct ticker 
    FROM {CHART_TABLE_NAME}
    order by ticker;
    '''
    df1 = pd.read_sql(sql_stmt, conn)
    conn.close()
    return df1['ticker'].to_list()

def _reformat_df_from_db(df):
    """rename columns for charting, parse date, set_index
    
        pd.to_datetime('20220406')
        # Timestamp('2022-04-06 00:00:00')    
    """
    df.rename(columns={'date_' : "Date", 'open_': "Open", 'high_':"High", 
                   'low_':"Low", 'close_':"Close", 'vol':"Volume"}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index("Date", inplace=True)
    return df

@st.cache()
def _query_chart_data(tickers, date_range):
    tickers_str = str(tickers).replace('[','(').replace(']',')')
    conn = sqlite3.connect(FILE_DB)
    sql_stmt = f'''
    SELECT * 
    FROM {CHART_TABLE_NAME} 
    where ticker in {tickers_str} 
        and date_ between '{date_range[0]}' and '{date_range[1]}'
    order by ticker, date_
    '''
    df = pd.read_sql(sql_stmt, conn)
    conn.close()
    return _reformat_df_from_db(df)

def _in_us_session(now_str=None):
    if now_str is None:
        now_str = datetime.strftime(datetime.now(), '%H:%M:%S')
    return now_str >= '09:30:00' and now_str <= '16:00:00'

def _parse_tickers(s):
    tmp = {}
    for t in [i.strip().upper() for i in re.sub('[^0-9a-zA-Z]+', ' ', s).split() if i.strip()]:
        tmp[t] = 1
    return list(tmp.keys())

def _title_xy(ticker):
    # position title manually
    return {"title": f"{ticker}",  "x": 0.55, "y": 0.945}

def _color_rsi_avg(v):
    if v > 0: return '#DCF7E5'
    elif v < 0: return '#F6D5F7'
    return YELLOW

def _color_signal(v):
    if v > 0: return 'g'
    elif v < 0: return 'r'
    return YELLOW

def _finviz_chart_url(ticker, period="d"):
    return f"https://finviz.com/quote.ashx?t={ticker}&p={period}"

QUOTE_TTL = 900 if _in_us_session() else 10800  # cache quote shorter if in-session
# st.write(f"QUOTE_TTL={QUOTE_TTL}")
@st.experimental_memo(ttl=QUOTE_TTL)
def _download_quote(symbol, num_days=NUM_DAYS_QUOTE):
    return yf.Ticker(symbol).history(f"{num_days}d")

def _get_quotes(symbol, num_days=NUM_DAYS_QUOTE, cache=False):
    """
    check cache:
        import pickle
        df = pickle.load(open("df_quotes_cache.pickle", "rb"))
        df.keys()
    """
    if not cache:
        return _download_quote(symbol, num_days=num_days)
        
    if Path.exists(FILE_CACHE_QUOTES):
        quote_data = pickle.load(open(FILE_CACHE_QUOTES, "rb"))
        if symbol in quote_data and num_days == quote_data[symbol]["num_days"]:
            df = quote_data[symbol]["df"]
        else:
            df = _download_quote(symbol, num_days=num_days)
            quote_data[symbol] = dict(num_days=num_days, df=df)
            pickle.dump(quote_data, open(FILE_CACHE_QUOTES, "wb"))
    else:
        df = _download_quote(symbol, num_days=num_days)
        quote_data = {}
        quote_data[symbol] = dict(num_days=num_days, df=df)
        pickle.dump(quote_data, open(FILE_CACHE_QUOTES, "wb"))

    return df

def _ta_MACD(df, fast_period=MACD_FAST, slow_period=MACD_SLOW, signal_period=MACD_SIGNAL):
    ema_fast = df["Close"].ewm(span=fast_period).mean()
    ema_slow = df["Close"].ewm(span=slow_period).mean()
    df["macd"] = ema_fast - ema_slow
    df["macd_signal"] = df["macd"].ewm(span=signal_period).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    return df

def _ta_RSI(df, n=RSI_PERIOD, avg_period=RSI_AVG, band_width=RSI_BAND_WIDTH):
    # https://github.com/wgong/mplfinance/blob/master/examples/rsi.py
    diff = df.w_p.diff().values
    gains = diff
    losses = -diff
    with np.errstate(invalid='ignore'):
        gains[(gains<0)|np.isnan(gains)] = 0.0
        losses[(losses<=0)|np.isnan(losses)] = 1e-10 # we don't want divide by zero/NaN
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = np.nanmean(gains[:n])
    l = losses[n] = np.nanmean(losses[:n])
    gains[:n] = losses[:n] = np.nan
    for i,v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i,v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    df['rsi'] = 50 - (100/(1+rs))
    df["rsi_avg"] = df.rsi.ewm(span=avg_period).mean()
    df["rsi_u"] = df["rsi_avg"] + band_width
    df["rsi_d"] = df['rsi_avg'] - band_width
    df["rsi_signal"] = df["rsi"] - df["rsi_avg"]
    return df

def _calculate_ta(df):
    df["w_p"] = 0.25*(2*df["Close"] + df["High"] + df["Low"])
    df["ema_fast"] = df.w_p.ewm(span=EMA_FAST).mean()
    df["ema_slow"] = df.w_p.ewm(span=EMA_SLOW).mean()
    df["ema_long"] = df.w_p.ewm(span=EMA_LONG).mean()

    # range
    hl_mean_fast = (df.High - df.Low).ewm(span=EMA_FAST).mean()
    df["ema_fast_u"] =  df.ema_fast + 0.5*hl_mean_fast * EMA_FAST_SCALE
    df["ema_fast_d"] =  df.ema_fast - 0.5*hl_mean_fast * EMA_FAST_SCALE

    hl_mean_slow = (df.High - df.Low).ewm(span=EMA_SLOW).mean()
    df["ema_slow_u"] =  df.ema_slow + 0.5*hl_mean_slow * EMA_SLOW_SCALE
    df["ema_slow_d"] =  df.ema_slow - 0.5*hl_mean_slow * EMA_SLOW_SCALE

    # trim volume to avoid exponential form
    df['Volume'] = df['Volume'] / 1000000
    df["vol_avg"] = df.Volume.ewm(span=MA_VOL).mean()

    return _ta_RSI(df)   

def _gen_chart_v1(ticker, df, num=0, chart_root="images",
                panid_price=PANID_PRICE, panid_vol=PANID_VOL,
                panid_rsi=PANID_RSI, panid_signal=PANID_SIGNAL):
    """
    Generate chart using Mplfinance
    """
    # candle overlay
    ema_fast_u_plot = mpf.make_addplot(df["ema_fast_u"], panel=panid_price, color=LIGHT_BLACK, linestyle="solid")
    ema_fast_d_plot = mpf.make_addplot(df["ema_fast_d"], panel=panid_price, color=LIGHT_BLACK, linestyle="solid")
    ema_slow_plot = mpf.make_addplot(df["ema_slow"], panel=panid_price, color='b', width=2, linestyle="solid")
    ema_long_plot = mpf.make_addplot(df["ema_long"], panel=panid_price, width=2, color='k')  # magenta
    
    # RSI
    # make sure ylim are the same
    rsi_min, rsi_max = np.nanmin(df["rsi"]), np.nanmax(df["rsi"])
    rsi_avg_plot2 = mpf.make_addplot(df["rsi_avg"], panel=panid_rsi, color="b", width=1, linestyle="solid",
                            ylim=(rsi_min,rsi_max))
    rsi_plot = mpf.make_addplot(df["rsi"], panel=panid_rsi, color='r', width=1, #title=f"{ticker}-RSI",
                            fill_between=dict(y1=df["rsi_d"].values,y2=df["rsi_u"].values,alpha=0.15,color='b'),
                            ylim=(rsi_min,rsi_max))
    rsi_avg_plot = mpf.make_addplot(df["rsi_avg"], panel=panid_rsi, type="bar", 
                            color=[_color_rsi_avg(v)  for v in df["rsi_avg"]], 
                            ylim=(rsi_min,rsi_max))
    signal_plot = mpf.make_addplot(df["rsi_signal"], panel=panid_signal, type="bar", 
                            color=[_color_signal(v) for v in df["rsi_signal"]], 
                            ylim=(-1,1))                            

    # volume
    vol_avg_plot = mpf.make_addplot(df["vol_avg"], panel=panid_vol, color='k')

    # plot
    plots = [
            # panel-0
            ema_fast_u_plot, ema_fast_d_plot, ema_slow_plot, ema_long_plot # ema_slow_u_plot, ema_slow_d_plot, 
            # panel-1
            , rsi_avg_plot, rsi_plot, rsi_avg_plot2  # , rsi_u_plot, rsi_d_plot 
            # panel-2
            , vol_avg_plot
            # panel-3
            , signal_plot
        ]
    file_img = join(chart_root, f"{ticker}-{str(num).zfill(2)}.png")
    # print(file_img)
    mpf.plot(df, type='candle', 
            style='yahoo', 
            fill_between=dict(y1=df["ema_fast_d"].values,y2=df["ema_fast_u"].values,alpha=0.15,color='b'),
            panel_ratios=PANEL_RATIOS,
            addplot=plots, 
            title=_title_xy(ticker),
            volume=True, volume_panel=panid_vol, 
            ylabel="", ylabel_lower='',
            xrotation=0,
            datetime_format='%Y-%m-%d',
            savefig=file_img,
            figsize=(FIGURE_WIDTH,FIGURE_HEIGHT),
            tight_layout=True,
            show_nontrading=True
        )  
    return {"ticker": ticker, "file_img": file_img}

def _gen_chart_v0(ticker, df, num=0, chart_root="images",
                panid_price=PANID_PRICE, panid_vol=PANID_VOL,
                panid_rsi=PANID_RSI, panid_signal=PANID_SIGNAL):
    """
    Generate chart using Mplfinance
    """
    # candle overlay
    ema_fast_u_plot = mpf.make_addplot(df["ema_fast_u"], panel=panid_price, color=LIGHT_BLACK, linestyle="solid")
    ema_fast_d_plot = mpf.make_addplot(df["ema_fast_d"], panel=panid_price, color=LIGHT_BLACK, linestyle="solid")
    ema_slow_plot = mpf.make_addplot(df["ema_slow"], panel=panid_price, color='b', linestyle="solid")
    ema_long_plot = mpf.make_addplot(df["ema_long"], panel=panid_price, width=2, color='k')  # magenta '#ED8CEB'
    
    # RSI
    # make sure ylim are the same
    rsi_min, rsi_max = np.nanmin(df['rsi']), np.nanmax(df['rsi'])
    rsi_plot = mpf.make_addplot(df["rsi"], panel=panid_rsi, color='r', width=1,  ylim=(rsi_min,rsi_max))
    rsi_avg_plot = mpf.make_addplot(df["rsi_avg"], panel=panid_rsi, 
        color='b', linestyle="dashed", ylim=(rsi_min,rsi_max))
    rsi_u_plot = mpf.make_addplot(df["rsi_u"], panel=panid_rsi, 
        color='b', linestyle="solid", ylim=(rsi_min,rsi_max))
    rsi_d_plot = mpf.make_addplot(df["rsi_d"], panel=panid_rsi, 
        color='b', linestyle="solid", ylim=(rsi_min,rsi_max))  # , ylabel=ticker)
    signal_plot = mpf.make_addplot(df["rsi_signal"], panel=panid_signal, type="bar", 
                            color=[_color_signal(v) for v in df["rsi_signal"]],ylim=(-1,1))                            

    # volume
    vol_avg_plot = mpf.make_addplot(df["vol_avg"], panel=panid_vol, color='k')

    # plot
    plots = [ema_fast_u_plot, ema_fast_d_plot, ema_slow_plot, ema_long_plot  
            , rsi_avg_plot, rsi_u_plot, rsi_d_plot, rsi_plot 
            , vol_avg_plot  
            , signal_plot                             
        ]
    # custom style
    # https://stackoverflow.com/questions/68296296/customizing-mplfinance-plot-python
    
    file_img = Path.joinpath(chart_root, f"{ticker}-{str(num).zfill(2)}.png")
    mpf.plot(df, type='candle', 
            style='yahoo', 
            fill_between=dict(y1=df["ema_fast_d"].values,y2=df["ema_fast_u"].values,alpha=0.15,color='b'),
            panel_ratios=PANEL_RATIOS,
            addplot=plots, 
            title=_title_xy(ticker),
            volume=True, volume_panel=panid_vol, 
            ylabel="", ylabel_lower="",
            xrotation=0,
            datetime_format='%m-%d',
            savefig=file_img,
            figsize=(st.session_state["FIGURE_WIDTH"],st.session_state["FIGURE_HEIGHT"]),
            tight_layout=True,
            show_nontrading=True
        )
    return {"ticker": ticker, "file_img": file_img}

# @st.experimental_memo(ttl=7200)
def _chart(ticker, chart_root=CHART_ROOT, panid_price=PANID_PRICE, panid_vol=PANID_VOL, 
        panid_rsi=PANID_RSI, panid_signal=PANID_SIGNAL):
    try:
        df = _get_quotes(ticker)
    except:
        err_msg = format_exc()
        return {"ticker": ticker, "err_msg": f"_get_quotes()\n{err_msg}"}

    try:
        df = _calculate_ta(df)
    except:
        err_msg = format_exc()
        return {"ticker": ticker, "err_msg": f"_calculate_ta()\n{err_msg}"}

    # slice after done with calculating TA 
    df = df.iloc[-NUM_DAYS_PLOT:, :]    

    x = _gen_chart_v0(ticker, df, chart_root=chart_root)
    # st.dataframe(df)   # ["Close", "Low", "High", "Volume"]
    _date, _today_quote, _prev_day_quote = df.iloc[-1, :].name, df.iloc[-1, :].to_dict(), df.iloc[-2, :].to_dict()
    # del [df, plots]  
    return {"ticker": ticker, "file_img": x["file_img"], "date": _date, "today_quote": _today_quote, "prev_day_quote": _prev_day_quote, "err_msg": None}

##############################################
## st handlers
##############################################
def go_home():
    st.subheader("Welcome")
    st.markdown("""
    This [app](https://github.com/wgong/watchetf/blob/main/app.py) is made with 
    - [yahoo-finance](https://github.com/ranaroussi/yfinance) for datafeed
    - [pandas](https://github.com/pandas-dev/pandas) for data-processing & analysis
    - [mplfinance](https://github.com/matplotlib/mplfinance) for chart
    - [streamlit](https://github.com/streamlit) <sub>an easy framework</sub> for layout
    
    """, unsafe_allow_html=True)
    
def _reformat_quote(ticker_dict):
    date = pd.to_datetime(ticker_dict["date"]).date()  # convert timestamp to datetime
    ticker = ticker_dict["ticker"]
    low_1 = f'{ticker_dict["prev_day_quote"]["Low"]:.2f}'
    high_1 = f'{ticker_dict["prev_day_quote"]["High"]:.2f}'
    close_1 = f'{ticker_dict["prev_day_quote"]["Close"]:.2f}'
    low = f'{ticker_dict["today_quote"]["Low"]:.2f}'
    high = f'{ticker_dict["today_quote"]["High"]:.2f}'
    close = f'{ticker_dict["today_quote"]["Close"]:.2f}'
    chg = 100*(1- ticker_dict["prev_day_quote"]["Close"] / ticker_dict["today_quote"]["Close"])
    return [date, ticker, chg, close, low, high, close_1, low_1, high_1]

def do_gwg_chart():
    if "chart_params" not in st.session_state: 
        return

    selected_tickers, chart_date_range = st.session_state["chart_params"]
    df_all = _query_chart_data(selected_tickers, chart_date_range)
    for ticker in selected_tickers:
        df = df_all[df_all['ticker'] == ticker]
        x = _gen_chart_v1(ticker, df)
        st.image(x["file_img"])

def do_mpl_chart():
    """ chart new ticker
    """
    quote_data = []
    tickers = st.text_input(f'Enter ticker(s) (max {MAX_NUM_TICKERS})', "SPY") 
    for ticker in _parse_tickers(tickers)[:MAX_NUM_TICKERS]:
        st.markdown(f"[{ticker}]({_finviz_chart_url(ticker)}) {ticker_name.get(ticker, '')}", unsafe_allow_html=True)
        ticker_dict = _chart(ticker)
        err_msg = ticker_dict["err_msg"]
        if err_msg:
            st.error(f"Failed ticker: {ticker}\n{err_msg}")
            continue
        file_img = ticker_dict["file_img"]
        if file_img:
            quote_data.append(_reformat_quote(ticker_dict))
            st.image(Image.open(file_img))
            
    st.dataframe(pd.DataFrame(quote_data, columns=QUOTE_COLUMNS), height=800)

def do_review(chart_root=CHART_ROOT):
    """ review existing charts
    """
    tickers = sorted([f.stem for f in Path(chart_root).glob("*.png")])
    selected_tickers = st.multiselect("Select tickers", tickers, [])
    for ticker in selected_tickers:
        file_img = Path.joinpath(chart_root, f"{ticker}.png")
        st.image(Image.open(file_img))
        st.markdown(f"[{ticker}]({_finviz_chart_url(ticker)})", unsafe_allow_html=True)

def do_show_etf_data():
    st.dataframe(etf_df)
    st.markdown(WATCH_ETF,unsafe_allow_html=True)

def do_show_etf_chart():
    """ ETF charts
    """
    period_item = st.session_state.get("period", "daily")
    period = PERIOD_DICT[period_item]

    for sect in st.session_state.get("selected_sectors", DEFAULT_SECTORS):
        st.subheader(sect)
        for k,v in etf_dict[sect].items():
            st.image(f"https://finviz.com/chart.ashx?t={k}&p={period}")
            st.markdown(f" [{k}]({_finviz_chart_url(k, period)}) : {v} ", unsafe_allow_html=True)
            # don't know how to get futures chart img


#####################################################
# menu_items
#####################################################

menu_dict = {
    _STR_HOME : {"fn": go_home},
    _STR_CHART: {"fn": do_mpl_chart},
    _STR_GWG_CHART: {"fn": do_gwg_chart},
    _STR_REVIEW_CHART: {"fn": do_review},
    _STR_ETF_CHART: {"fn": do_show_etf_chart},
    _STR_ETF_DATA: {"fn": do_show_etf_data},
}

## sidebar Menu
def do_sidebar():
    menu_options = list(menu_dict.keys())
    default_ix = menu_options.index(_STR_HOME)
    
    with st.sidebar:
        st.header(_STR_APP_NAME)

        menu_item = st.selectbox("Select", menu_options, index=default_ix, key="menu_item")

        if menu_item == _STR_ETF_CHART:
            st.selectbox('Period:', list(PERIOD_DICT.keys()), index=0, key="period")
            st.multiselect("Sectors", etf_sectors, DEFAULT_SECTORS, key="selected_sectors")


        if menu_item == _STR_REVIEW_CHART:
            st.image(BACKGROUND_IMG_URL)  # padding
            st.image(BACKGROUND_IMG_URL)
            btn_cleanup = st.button("Cleanup charts")
            if btn_cleanup:
                for f in Path(CHART_ROOT).glob("*.png"):
                    f.unlink()

        if menu_item == _STR_CHART:
            st.number_input("Figure width", value=FIGURE_WIDTH, key="FIGURE_WIDTH")
            st.number_input("Figure height", value=FIGURE_HEIGHT, key="FIGURE_HEIGHT")

        if menu_item == _STR_GWG_CHART:
            dummy_item = ' _ '
            _tickers = _query_tickers()
            selected_tickers = st.multiselect("Tickers", _tickers, ['QQQ'], key="selected_tickers")
            list_date_ranges = [f"{dr[0]} _ {dr[1]}" for dr in _make_date_ranges()]
            list_date_ranges.insert(0, dummy_item)
            _date_range = st.selectbox('Date range', list_date_ranges, index=0, key="date_range")
            if _date_range and _date_range != dummy_item:
                dr_1, dr_2 = _date_range.split(dummy_item)
                to_date = pd.to_datetime(dr_2)
                from_date = pd.to_datetime(dr_1)
            else:
                to_date = datetime.now()
                from_date = to_date + timedelta(days=-NUM_DAYS_PLOT)
            col_left,col_right = st.columns(2)
            with col_left:
                begin_date = st.date_input("Begin date", from_date.date(), key="begin_date")
            with col_right:
                end_date = st.date_input("End date", to_date.date(), key="end_date")
            chart_date_range = (datetime.strftime(begin_date, '%Y%m%d'), datetime.strftime(end_date, '%Y%m%d'))
            # st.write(selected_tickers, chart_date_range)
            st.session_state["chart_params"] = selected_tickers, chart_date_range

# body
def do_body():
    menu_item = st.session_state.menu_item  
    menu_dict[menu_item]["fn"]()


def main():
    do_sidebar()
    do_body()

if __name__ == '__main__':
    main()
