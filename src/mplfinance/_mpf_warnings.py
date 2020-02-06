import sys as __sys
if not __sys.warnoptions:
    import os as __os
    import warnings as __warnings
    __warnings.filterwarnings("default",category=DeprecationWarning,module='mplfinance') # Change the filter in this process
    __os.environ["PYTHONWARNINGS"] = "default::DeprecationWarning:mplfinance"            # Also affect subprocesses
