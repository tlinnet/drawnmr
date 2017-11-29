"""# Get import"""
from drawnmr import draw
import nmrglue as ng
import bokeh.plotting as bplt
from bokeh.models import Range1d

"""# Get data"""
# Get data
import os, os.path
ng_dir = 'nmrglue_data/s4_2d_plotting'
if not os.path.exists(ng_dir):
    print("No %s. Downloading."%ng_dir)
    import urllib.request, zipfile
    zipf = 'jbnmr_s4_2d_plotting.zip'
    urllib.request.urlretrieve('https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/nmrglue/%s'%zipf, zipf)
    with zipfile.ZipFile(zipf,"r") as zip_ref:
        zip_ref.extractall("nmrglue_data")
    os.remove(zipf)

"""# Read data"""
# Specify data
ng_ft2 = 'nmrglue_data/s4_2d_plotting/test.ft2'

# read in data
ng_dic, ng_data = ng.pipe.read(ng_ft2)

"""# Create figure"""
# Pass to figure class
fig2d = draw.fig2d(ng_dic, ng_data)
# Change contour_start
fig2d.contour_start = 8.5e4

# Get the boheh figure
fig= fig2d.get_fig()

"""# Alter figure"""
# Alter the figure after creation
fig.xaxis.axis_label = "Nonsense"
# Set limits
fig.x_range = Range1d(183.5, 167.5)
fig.y_range = Range1d(139.5, 95.5)

"""# Show output"""
# Get output. Either to Jupyter notebook or html file 
if fig2d.isnotebook():
    from bokeh.io import output_notebook
    output_notebook()
    bplt.show(fig)
else:
    # Save to html
    filename = "nmrglue_s4_2d_plotting.html"
    bplt.output_file(filename)
    bplt.save(fig)
    # And auto open
    import webbrowser, os
    webbrowser.open('file://' + os.path.realpath(filename))