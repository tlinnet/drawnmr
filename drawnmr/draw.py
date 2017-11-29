import nmrglue as ng
from matplotlib.contour import QuadContourSet
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import bokeh.plotting as bplt
from bokeh.models import ColumnDataSource, Range1d, WidgetBox, LassoSelectTool, BoxZoomTool, BoxSelectTool, HoverTool
from bokeh.models.widgets import Slider, Panel, Tabs
from bokeh.io import push_notebook

class fig2d:
    def __init__(self, ng_dic=None, ng_data=None):
        self.dic = ng_dic
        self.data = ng_data

        # Get Universal dictionary
        # for uniform listing of spectal parameter
        self.udic = ng.pipe.guess_udic(ng_dic, ng_data)
        
        # reference data in more common NMR units using the unit_coversion object.
        self.uc0 = ng.pipe.make_uc(self.dic, self.data, dim=0) # m, rows, y-axis
        self.uc1 = ng.pipe.make_uc(self.dic, self.data, dim=1) # n, columns, x-axis

        # Get ppm limits
        self.x0_ppm, self.x1_ppm = self.uc1.ppm_limits()
        self.y0_ppm, self.y1_ppm = self.uc0.ppm_limits()
        
        # Calculate ppm range
        self.x_ppm_scale = self.uc1.ppm_scale()
        self.y_ppm_scale = self.uc0.ppm_scale()

        # Set default values
        # contour level start value
        self.contour_start =  8.5e4
        # number of contour levels
        self.contour_num = 20
        # scaling factor between contour levels
        self.contour_factor = 1.20

    def isnotebook(self):
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                # Jupyter notebook or qtconsole
                return True
            elif shell == 'TerminalInteractiveShell':
                # Terminal running IPython
                return False
            else:
                # Other type (?)
                return False
        except NameError:
             # Probably standard Python interpreter
            return False

    def get_contour_levels(self):
        # calculate contour levels
        cl = [self.contour_start * self.contour_factor ** x for x in range(self.contour_num)]
        return cl

    def get_contours(self):
        # Use method matplotlib
        fig = Figure()
        ax = Axes(fig, [0, 0, 1, 1])
        # Get extent
        extent=(self.x0_ppm, self.x1_ppm, self.y0_ppm, self.y1_ppm)
        # calculate contour levels
        cl = self.get_contour_levels()
        # Get contours
        contour_set = QuadContourSet(ax, self.data, filled=False, extent=extent, levels=cl)

        # To plot in bokeh
        xs = []
        ys = []
        xt = []
        yt = []
        col = []
        text = []
        isolevelid = 0
        for isolevel in contour_set.collections:
            theiso = str(contour_set.get_array()[isolevelid])
            # Get colour
            isocol = isolevel.get_color()[0]
            thecol = 3 * [None]
            for i in range(3):
                thecol[i] = int(255 * isocol[i])
            thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

            for path in isolevel.get_paths():
                v = path.vertices
                x = v[:, 0]
                y = v[:, 1]
                xs.append(x.tolist())
                ys.append(y.tolist())
                xt.append(x[int(len(x) / 2)])
                yt.append(y[int(len(y) / 2)])
                text.append(theiso)
                col.append(thecol)
            # Add to counter
            isolevelid += 1
        cdata={'xs': xs, 'ys': ys, 'line_color': col}
        ctext={'xt':xt,'yt':yt,'text':text}
        return cdata, ctext
    
    def get_fig(self):
        # Make figure
        #tools = "pan, wheel_zoom, box_zoom, reset, box_select, lasso_select, help"
        fig = bplt.figure(plot_width=400,plot_height=400, x_range=(self.x0_ppm, self.x1_ppm), y_range=(self.y0_ppm, self.y1_ppm))
        # Add tools
        #fig.add_tools(LassoSelectTool())
        #fig.add_tools(BoxSelectTool())
        #fig.add_tools(HoverTool())
        fig.add_tools(HoverTool(tooltips=[
                #("index", "$index"),
                ("(x,y)", "($x, $y)"),
                #("desc", "@desc")
                ]))

        # Get contour paths
        cdata, ctext = self.get_contours()
        # Define figure source
        source = ColumnDataSource(cdata)
        fig.multi_line(xs='xs', ys='ys', line_color='line_color', source=source)
        #fig.text(x='xt',y='yt',text='text',source=source,text_baseline='middle',text_align='center')

        # Set label
        fig.xaxis.axis_label = self.udic[1]['label'] + ' ppm'
        fig.yaxis.axis_label = self.udic[0]['label'] + ' ppm'

        # Set limits
        fig.x_range = Range1d(183.5, 167.5)
        fig.y_range = Range1d(139.5, 95.5)

        return fig