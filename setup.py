from setuptools import setup
from setuptools import find_packages

setup(name='mplfinance',
      version='0.11.0',
      author='MPL Developers',
      author_email='matplotlib-users@python.org',
      py_modules=['mplfinance'],
      description='Finance plots using matplotlib',
      url='http://github.com/matplotlib/mplfinance',
      platforms='Cross platform (Linux, Mac OSX, Windows)',
      install_requires=['matplotlib'],
      license="BSD",
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      keywords='finance',
      )
