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

How to install?
--------------------
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
   
