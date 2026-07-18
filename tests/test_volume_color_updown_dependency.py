"""
Regression tests for the `volume_color_updown_dependency` setting, which controls
how the up/down color of each volume bar is decided:

    "Open vs Close"    (default) : today's open  vs today's close (same as candles)
    "Previous Close"             : today's close vs the previous close
    "Previous Volume"            : today's volume vs the previous volume

Value matching is case- and space-insensitive.  The setting can be provided via
`make_marketcolors()`, `make_mpf_style()`, or directly as a `plot()` kwarg, and it
is backward compatible with the legacy `vcdopcod` setting.
"""

import numpy             as np
import pandas            as pd
import mplfinance        as mpf
import matplotlib.pyplot as plt
import pytest

print('mpf.__version__ =', mpf.__version__)                  # for the record


def _sample_df():
    idx   = pd.date_range('2024-01-01', periods=8, freq='D')
    close = np.array([10, 11, 10.5, 12, 11.8, 13, 12.5, 14.0])
    # Volume deliberately rises/falls independently of price, so that the
    # 'Previous Volume' coloring is distinguishable from the price-based modes.
    vol   = np.array([100, 80, 120, 90, 150, 60, 200, 50.0])
    df = pd.DataFrame({'Open': close - 0.2, 'High': close + 0.5,
                       'Low': close - 0.5, 'Close': close, 'Volume': vol}, index=idx)
    df.index.name = 'Date'
    return df


def _bar_colors(fig, axlist):
    volume_ax = axlist[2]  # panel holding the volume bars
    colors = [tuple(np.round(patch.get_facecolor(), 3)) for patch in volume_ax.patches]
    plt.close(fig)
    return colors


def _base_marketcolors(**mc_kwargs):
    return mpf.make_marketcolors(up='g', down='r', volume={'up': 'g', 'down': 'r'}, **mc_kwargs)


def _colors_via_marketcolors(df, **mc_kwargs):
    style = mpf.make_mpf_style(marketcolors=_base_marketcolors(**mc_kwargs))
    return _bar_colors(*mpf.plot(df, type='candle', volume=True, style=style, returnfig=True))


def _colors_via_plot_kwarg(df, mode):
    style = mpf.make_mpf_style(marketcolors=_base_marketcolors())
    return _bar_colors(*mpf.plot(df, type='candle', volume=True, style=style,
                                 volume_color_updown_dependency=mode, returnfig=True))


def _colors_via_make_mpf_style(df, mode):
    style = mpf.make_mpf_style(marketcolors=_base_marketcolors(),
                               volume_color_updown_dependency=mode)
    return _bar_colors(*mpf.plot(df, type='candle', volume=True, style=style, returnfig=True))


def test_volume_color_modes_differ():
    df = _sample_df()
    open_vs_close = _colors_via_marketcolors(df, volume_color_updown_dependency='Open vs Close')
    previous_vol  = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Volume')
    assert previous_vol != open_vs_close
    assert len(previous_vol) == len(df)


def test_case_and_space_insensitive():
    df = _sample_df()
    canonical = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Volume')
    for variant in ('previous volume', 'PREVIOUSVOLUME', '  Previous  Volume '):
        assert _colors_via_marketcolors(df, volume_color_updown_dependency=variant) == canonical


def test_backward_compatible_with_vcdopcod():
    df = _sample_df()
    legacy   = _colors_via_marketcolors(df, vcdopcod=True)
    explicit = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Close')
    assert legacy == explicit


def test_settable_via_plot_kwarg():
    df = _sample_df()
    via_plot         = _colors_via_plot_kwarg(df, 'Previous Volume')
    via_marketcolors = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Volume')
    assert via_plot == via_marketcolors


def test_settable_via_make_mpf_style():
    df = _sample_df()
    via_style        = _colors_via_make_mpf_style(df, 'Previous Volume')
    via_marketcolors = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Volume')
    assert via_style == via_marketcolors


def test_plot_kwarg_overrides_style_setting():
    df = _sample_df()
    # Style says 'Open vs Close', but the plot() kwarg should take precedence.
    style = mpf.make_mpf_style(marketcolors=_base_marketcolors(),
                               volume_color_updown_dependency='Open vs Close')
    overridden = _bar_colors(*mpf.plot(df, type='candle', volume=True, style=style,
                                       volume_color_updown_dependency='Previous Volume',
                                       returnfig=True))
    pure_previous_vol = _colors_via_marketcolors(df, volume_color_updown_dependency='Previous Volume')
    assert overridden == pure_previous_vol


def test_invalid_value_raises():
    for maker in (lambda v: mpf.make_marketcolors(volume_color_updown_dependency=v),
                  lambda v: mpf.make_mpf_style(volume_color_updown_dependency=v)):
        with pytest.raises(Exception):
            maker('not a real mode')
