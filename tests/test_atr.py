import pandas as pd

from mplfinance._utils import _calculate_atr


def test_atr_indexes_datetime_series_by_position():
    index = pd.date_range("2020-01-01", periods=5, freq="D")
    high = pd.Series([10, 12, 11, 13, 12], index=index)
    low = pd.Series([8, 9, 9, 10, 9], index=index)
    close = pd.Series([9, 11, 10, 12, 11], index=index)

    # Bars 4 and 5 each have a true range of 3, so a 2-bar ATR is 3.
    assert _calculate_atr(2, high, low, close) == 3
    assert _calculate_atr(2, high.to_numpy(), low.to_numpy(), close.to_numpy()) == 3
    assert _calculate_atr(2, list(high), list(low), list(close)) == 3
