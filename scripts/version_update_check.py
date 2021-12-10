import os
import sys
import importlib
from   packaging import version

if len(sys.argv) < 3:
   raise RuntimeError('Got less than 2 Version Arguments!')

debug = True if (len(sys.argv) > 3 and sys.argv[3] == 'debug') else False

v0  = importlib.import_module(sys.argv[1])
pv0 = version.parse(v0.__version__)

v1  = importlib.import_module(sys.argv[2])
pv1 = version.parse(v1.__version__)

if debug:
    print('sys.argv=',sys.argv)
    print('v0=',v0)
    print('v1=',v1)
    print('pv0=',pv0)
    print('pv1=',pv1)
#   cmd='cat '+sys.argv[1]+'.py'
#   print('os.system("'+cmd+'")')
#   os.system(cmd)
#   cmd='cat '+sys.argv[2]+'.py'
#   print('os.system("'+cmd+'")')
#   os.system(cmd)
    print('v0.__version__=',v0.__version__)
    print('v1.__version__=',v1.__version__)

if not pv1 > pv0:
    print('ERROR: Pull Request requires mplfinance version to be updated: (Version '+str(pv1)+' is NOT greater than '+str(pv0)+')')
    exit(1)
else:
    print('Version was updated OK (from '+str(pv0)+' to '+str(pv1)+')')
    exit(0)
