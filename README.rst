=======
drawnmr 
=======

What is drawnmr?
----------------

drawnmr is a module for viewing NMR data in Python. When used with the
nmrglue and bokeh packages, drawnmr provides functions to view and
interact with NMR data.

nmrglue is used for processing nmrdata, and bokeh is used
for showing and interacting. A range of widgets is written to interact 
with the plot.

Important Links
---------------

* Source code: https://github.com/tlinnet/drawnmr
* Link to nmrglue: https://www.nmrglue.com and https://github.com/jjhelmus/nmrglue
* Link to bokeh: https://bokeh.pydata.org and https://github.com/bokeh/bokeh

What can drawnmr do?
--------------------

drawnmr is a wrapper around nmrglue capabilities and provide helper functions
to show the data in boheh, which is an interactive visualization library.

The main purpose is to show NMR data in a Jupyter Notebook.
If a Jupyter Notebook installation is not running, bokeh allow
the output to be saved to static HTML files.

Use interactive examples
------------------------

* Launch interactive Jupyter Notebook with mybinder.org and try examples:

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/tlinnet/drawnmr/master

* Or use nbviewer.jupyter.org to see the Notebook: nmrglue_s4_2d_plotting.ipynb_

.. _nmrglue_s4_2d_plotting.ipynb: http://nbviewer.jupyter.org/github/tlinnet/drawnmr/blob/master/examples/nmrglue_s4_2d_plotting.ipynb

.. image:: https://raw.githubusercontent.com/tlinnet/drawnmr/master/docs/images/image_2.png
.. image:: https://raw.githubusercontent.com/tlinnet/drawnmr/master/docs/images/image_1.png

How to install?
---------------
If using conda, these steps will install an environment

.. code-block:: bash

   # Create environment
   conda create -n py36 python=3.6
   
   # Install conda packages into environment
   conda install -y -n py36 --file conda_req.txt
   
   # Activate environment
   alias py36='source activate py36'
   source activate py36
   
   # pip install
   pip install -r requirements.txt

   # install package
   python setup.py install --force

Developer
---------

* Guide for upload: http://peterdowns.com/posts/first-time-with-pypi.html
* Updated info: https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
* PyPI test account: http://testpypi.python.org/pypi?%3Aaction=register_form 
* PyPI Live account: http://pypi.python.org/pypi?%3Aaction=register_form

.. code-block:: bash

   # Modify version in: drawnmr/__init__.py
   
   # Create tag
   VERS=`python -c "from drawnmr import __version__; print(__version__)"`
   # Adds a tag so that we can put this on PyPI
   git tag $VERS -m ""
   git push --tags origin master
   
   # Upload your package to PyPI Test
   python setup.py sdist upload -r pypitest
   open https://testpypi.python.org/pypi/drawnmr
   
   # Upload to PyPI Live
   # Once you've successfully uploaded to PyPI Test, perform the same steps but point to the live PyPI server instead.
   python setup.py sdist upload -r pypi
   open https://pypi.python.org/pypi/drawnmr