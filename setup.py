from setuptools import setup
from setuptools import find_packages

pkg_location = 'src'
pkg_name     = 'mplfinance'

vfile = './'+pkg_location+'/'+pkg_name+'/_version.py'
vers = {}
with open(vfile) as f:
   exec(f.read(), {}, vers)

with open('README.md') as f:
    long_description = f.read()

setup(name=pkg_name,
      version=vers['__version__'],
      author='MPL Developers',
      author_email='matplotlib-users@python.org',
      py_modules=[pkg_name],
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
