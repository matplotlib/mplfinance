import pytest
import pandas as pd
import numpy as np
import mplfinance as mpf
from mplfinance._utils import _get_traditional_box_size
print(mpf.__file__)
def make_df(prices):
    return pd.DataFrame({
        'Open': prices,
        'High': prices,
        'Low': prices,
        'Close': prices,
        'Volume': [100] * len(prices)
    }, index=pd.date_range("2024-01-01", periods=len(prices)))

def test_traditional_boundaries():
    assert _get_traditional_box_size(0.2) == 0.0625
    assert _get_traditional_box_size(0.25) == 0.125
    assert _get_traditional_box_size(1) == 0.25
    assert _get_traditional_box_size(5) == 0.5
    assert _get_traditional_box_size(20) == 1
    assert _get_traditional_box_size(100) == 2
    assert _get_traditional_box_size(200) == 4
    assert _get_traditional_box_size(500) == 5
    assert _get_traditional_box_size(1000) == 10

def test_traditional_runs():
    prices = [100, 102, 101, 105, 107, 103]
    df = make_df(prices)

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size='traditional'),
        returnfig=True
    )

def test_atr_no_crash():
    prices = [100, 100.2, 100.1, 100.15, 100.05]
    df = make_df(prices)

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size='atr'),
        returnfig=True
    )

def test_fixed_still_works():
    prices = [100, 102, 101, 103]
    df = make_df(prices)

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size=2),
        returnfig=True
    )

def test_low_price_range():
    prices = [0.1, 0.2, 0.3, 0.4, 0.5]
    df = make_df(prices)

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size='traditional'),
        returnfig=True
    )

def test_high_volatility():
    np.random.seed(0)
    prices = np.cumsum(np.random.randn(200)) + 100

    df = pd.DataFrame({
        'Open': prices,
        'High': prices + 1,
        'Low': prices - 1,
        'Close': prices,
        'Volume': [100] * len(prices)
    }, index=pd.date_range("2024-01-01", periods=len(prices)))

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size='traditional'),
        returnfig=True
    )

def test_scale_consistency():
    base = [10, 12, 11, 13, 15, 14]
    scaled = [x * 100 for x in base]

    df1 = make_df(base)
    df2 = make_df(scaled)

    mpf.plot(df1, type='pnf',
             pnf_params=dict(box_size='traditional'),
             returnfig=True)

    mpf.plot(df2, type='pnf',
             pnf_params=dict(box_size='traditional'),
             returnfig=True)

def test_fixed_still_works():
    prices = [100, 110, 105, 120]  # bigger range
    df = make_df(prices)

    mpf.plot(
        df,
        type='pnf',
        pnf_params=dict(box_size=2),
        returnfig=True
    )
def test_fixed_invalid_boxsize_raises():
    prices = [100, 102, 101, 103]
    df = make_df(prices)

    with pytest.raises(ValueError):
        mpf.plot(
            df,
            type='pnf',
            pnf_params=dict(box_size=2),
            returnfig=True
        )