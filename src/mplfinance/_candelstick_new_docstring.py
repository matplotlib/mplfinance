"""Represent today's open to close as a "bar" line (candle body)
and high low range as a vertical line (candle wick)

If config['type']=='hnf_candle' (hollow and filled candles) then
candle edge and wick color depend on PREVIOUS close to today's close (up or down),
and the center of the candle body depends on the today's open to close (up or down).
"""
