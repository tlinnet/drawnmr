#!/usr/bin/env python

# setup script for nmrglue

from distutils.core import setup
from codecs import open
from os import path
from drawnmr import __version__

here = path.abspath(path.dirname(__file__))

# get long description from README
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='drawnmr',
    version=__version__,
    description='A module for displaying NMR data with bokeh in Python or Jupyter Notebooks.',
    long_description=long_description,
    url='https://github.com/tlinnet/drawnmr',
    download_url='https://github.com/tlinnet/drawnmr/archive/%s.tar.gz'%__version__,
    author='Troels Schwarz-Linnet',
    author_email='tlinnet@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux'],
    requires=['bokeh', 'numpy', 'matplotlib', 'nmrglue', 'scipy'],
    packages=[
        'drawnmr'],
    data_files=[('', ['README.rst', 'LICENSE'])],
)