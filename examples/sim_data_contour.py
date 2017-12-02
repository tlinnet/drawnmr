"""# Get import"""
try:
    from drawnmr import draw
except ModuleNotFoundError:
    import sys, os
    sys.path.append( os.getcwd()+os.sep+"..")
    print(sys.path)

"""# Get import"""
from drawnmr import draw
import bokeh.plotting as bplt
import numpy as np

"""# Create data """
N = 500
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

"""# Create figure"""
# Pass to figure class
fig2d = draw.fig2d(ng_data=d)
# Change contour_start
fig2d.contour_start = -1.
fig2d.contour_factor = None

# Get the bokeh figure
fig= fig2d.get_fig()

"""# Get peaks"""
# Get positive peaks
peaks_p = fig2d.get_peakpick(pthres=0.7)
print(peaks_p.head(n=10))

# Get negative peaks
peaks_n = fig2d.get_peakpick(nthres=-0.7)
print(peaks_n.head(n=10))

"""# Show output"""
# Get output. Either to Jupyter notebook or html file 
if fig2d.isnotebook:
    from bokeh.io import output_notebook
    output_notebook()
    bplt.show(fig, notebook_handle=True)
else:
    # Save to html
    filename = "bokeh.html"
    bplt.output_file(filename)
    bplt.save(fig)
    # And auto open
    import webbrowser, os
    webbrowser.open('file://' + os.path.realpath(filename))


