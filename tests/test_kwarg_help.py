import os
import os.path
import glob
import mplfinance        as mpf

print('mpf.__version__ =',mpf.__version__)                 # for the record


def test_kwarg_help():

    functions = ['plot', 'make_addplot', 'make_marketcolors', 'make_mpf_style',
                 'renko_params', 'pnf_params', 'lines', 'scale_width_adjustment',
                 'update_width_config']

    # just call `kwarg_help()` for each function,
    #  and make sure there are no exceptions:

    mpf.kwarg_help()

    for func_name in functions:
        mpf.kwarg_help(func_name)

    # now call with `sort=True` (again, just making sure no exceptions)

    mpf.kwarg_help('plot',sort=True)
    
