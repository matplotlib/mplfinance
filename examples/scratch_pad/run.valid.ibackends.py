import matplotlib.pyplot as plt
import matplotlib as mpl
from   pylab import *

##  ==================================================================================
##  supported backends:     ['ps', 'webagg', 'qt4agg', 'agg', 'wx', 'svg', 'qt5agg',
##                           'template', 'gtk3cairo', 'pdf', 'qt5cairo', 'macosx', 
##                           'qt4', 'gtk3agg', 'nbagg', 'webagg_core', 'wxcairo',
##                           'qt5', 'gtk3', 'mixed', 'tkagg', 'qt4cairo', 'tkcairo',
##                           'wxagg', 'pgf', 'cairo']
##  valid backends:         ['ps', 'webagg', 'agg', 'svg', 'template', 'pdf', 'nbagg',
##                           'tkagg', 'pgf']
##  ps FPS:          1823.8522934563061
##  webagg FPS:      7169.995555403603
##  agg FPS:         20.852366968595575
##  svg FPS:         3809.921063866508
##  template FPS:    23.202661861618655
##  pdf FPS:         2901.3876399053693
##  <IPython.core.display.Javascript object>
##  <IPython.core.display.HTML object>
##  nbagg error :(
##  tkagg FPS:       2901.929636420244
##  pgf FPS:         5311.09436829276
##  ==================================================================================

x = arange(0,2*pi,0.01)

#for b in ['tkagg','webagg','nbagg']:
#for b in ['tkagg','nbagg']:
for b in ['tkagg','Qt5Agg']:
    mpl.use(b)
    print('Backend: ',plt.get_backend())
    plt.plot(x,sin(x))
    plt.show()
