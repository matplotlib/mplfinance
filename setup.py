from setuptools import setup
from setuptools import find_packages

pkg_location = 'src'

import sys
# Never sys.path.insert(0, ). Rather sys.path.insert(1, ) because
# third-party code may rely on sys.path documentation conformance:
#    As initialized upon program startup, the first item of this list, path[0], is
#    the directory containing the script that was used to invoke the Python interpreter.
###sys.path.insert(1,pkg_location)
# for safety, make sure this: is the only import after changing sys.path
###from mplfinance import __version__
__version__='0.11.0a0' # test hard-coded so avoid sys.path.insert (maybe that's breaking travis checks).

with open('README.md') as f:
    long_description = f.read()

setup(name='mplfinance',
      version=__version__,
      author='MPL Developers',
      author_email='matplotlib-users@python.org',
      py_modules=['mplfinance'],
      description='Utilities for the visualization, and visual analysis, of financial data',
      long_description=long_description,
      long_description_content_type='text/markdown; charset=UTF-8',
      url='http://github.com/matplotlib/mplfinance',
      platforms='Cross platform (Linux, Mac OSX, Windows)',
      install_requires=['matplotlib','pandas'],
      license="BSD-style",
      package_dir={'': pkg_location},
      packages=find_packages(where=pkg_location),
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      keywords='finance',
      )
