import yfinance as yf
import mplfinance as mpf
import pandas as pd

def prepare_data(ticker):
    data = yf.download(ticker, period="6mo")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)

    data = data.astype(float)

    return data


def test_atr_no_crash(data):
    print("\n[TEST] ATR scaling (should NOT crash)")
    try:
        mpf.plot(
            data,
            type='pnf',
            title="ATR Box Scaling Test",
            pnf_params=dict(box_size='atr'),
            savefig='test_atr.png'
        )
        print(" ATR test passed")
    except Exception as e:
        print(" ATR test failed:", e)


def test_traditional(data):
    print("\n[TEST] Traditional scaling")
    try:
        mpf.plot(
            data,
            type='pnf',
            title="Traditional Box Scaling Test",
            pnf_params=dict(box_size='traditional'),
            savefig='test_traditional.png'
        )
        print("Traditional test passed")
    except Exception as e:
        print(" Traditional test failed:", e)


def test_fixed(data):
    print("\n[TEST] Fixed box scaling")
    try:
        mpf.plot(
            data,
            type='pnf',
            title="Fixed Box Scaling Test",
            pnf_params=dict(box_size=2),
            savefig='test_fixed.png'
        )
        print(" Fixed test passed")
    except Exception as e:
        print(" Fixed test failed:", e)


if __name__ == "__main__":
    print("Using mplfinance from:")
    print(mpf.__file__)

    data1 = prepare_data("AAPL")
    data2 = prepare_data("TSLA")

    print("\n--- Running tests on AAPL ---")
    test_atr_no_crash(data1)
    test_traditional(data1)
    test_fixed(data1)

    print("\n--- Running tests on TSLA ---")
    test_atr_no_crash(data2)
    test_traditional(data2)
    test_fixed(data2)

    print("\nAll tests completed 🚀")