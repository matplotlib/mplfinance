        # extrapolate backward:
        loc_linear = _date_to_iloc_linear(dtseries,date)
        first = _date_to_mdate(dtseries.index[0])
        last  = _date_to_mdate(dtseries.index[-1])
        avg_days_between_points = (last - first)/float(len(dtseries))
        if avg_days_between_points > 0.33:  # daily (not intraday)
            delta      = _date_to_mdate(dtseries.index[0]) - _date_to_mdate(date)
            loc_5_7ths = - (5./7.)*delta
            loc = (loc_linear + loc_5_7ths)/2.0
        else:
            loc = loc_linear
        return loc
