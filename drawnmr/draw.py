import nmrglue as ng
import numpy as np
import bokeh.models as bm

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
        # contour level start value. Only the last 1 percent of data is normally interesting.
        self.contour_start =  np.percentile(self.data, 99)
        # number of contour levels
        self.contour_num = 20
        # scaling factor between contour levels
        self.contour_factor = 1.20

        # Create initial ColumnDataSource
        self.ColumnDataSource = None

        # Check notebook
        self.isnotebook = self.check_isnotebook()

    def check_isnotebook(self):
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
        from matplotlib.contour import QuadContourSet
        from matplotlib.axes import Axes
        from matplotlib.figure import Figure

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
        zs = []
        xt = []
        yt = []
        col = []
        text = []
        isolevelid = 0
        for level, isolevel in zip(cl, contour_set.collections):
            level_round = round(level, 2)
            #theiso = str(contour_set.get_array()[isolevelid])
            theiso = str(level_round)
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
                zs.append(level)
                xt.append(x[int(len(x) / 2)])
                yt.append(y[int(len(y) / 2)])
                text.append(theiso)
                col.append(thecol)
            # Add to counter
            isolevelid += 1
        cdata={'xs': xs, 'ys': ys, 'line_color': col, 'zs': zs}
        ctext={'xt':xt,'yt':yt,'text':text}
        return cdata, ctext

    def create_ColumnDataSource(self):
        # Get contour paths
        cdata, ctext = self.get_contours()

        # Create ColumnDataSource
        self.ColumnDataSource = bm.ColumnDataSource(cdata)
        self.ColumnDataSourceText = bm.ColumnDataSource(ctext)

    def change_contour_start(self, contour_start):
        # Update value
        self.contour_start = contour_start
        self.update_ColumnDataSource()

    def change_contour_start_w(self, change):
        self.contour_start = change['new']
        self.update_ColumnDataSource()

    def change_contour_num_w(self, change):
        self.contour_num = change['new']
        self.update_ColumnDataSource()

    def change_contour_factor_w(self, change):
        self.contour_factor = change['new']
        self.update_ColumnDataSource()

    def update_ColumnDataSource(self):
        from bokeh.io import push_notebook

        # Get contour paths
        cdata, ctext = self.get_contours()

        # Patches
        patches = {
            'xs' : [ (slice(None), cdata['xs']) ],
            'ys' : [ (slice(None), cdata['ys']) ],
            'line_color' : [ (slice(None), cdata['line_color']) ],
            'zs' : [ (slice(None), cdata['zs']) ],
            }

        # Apply patches
        self.ColumnDataSource.patch(patches)

        # Other method
        #self.fig_multi.data_source.data['xs'] = cdata['xs']
        #self.fig_multi.data_source.data['ys'] = cdata['ys']
        #self.fig_multi.data_source.data['line_color'] = cdata['line_color']
        #self.fig_multi.data_source.data['zs'] = cdata['zs']
        if self.isnotebook:
            push_notebook()
    
    def get_fig(self):
        import bokeh.plotting as bplt

        # Make tools
        wheel_zoom = bm.WheelZoomTool()
        self.hover = bm.HoverTool(tooltips=[
                #("index", "$index"),
                ("(x,y)", "($x, $y)"),
                ("int", "@zs"),
                ("VOL", "@VOL"),
                #("fill color", "$color[hex, swatch]:fill_color"),
                #("Color", "@line_color"),
                ])
        tools = [bm.PanTool(), bm.BoxZoomTool(), wheel_zoom, bm.SaveTool(), bm.ResetTool(), bm.UndoTool(), bm.RedoTool(), bm.CrosshairTool(), self.hover]
        # Make figure
        self.fig = bplt.figure(plot_width=400,plot_height=400, x_range=(self.x0_ppm, self.x1_ppm), y_range=(self.y0_ppm, self.y1_ppm), tools=tools)
        # Activate scrool
        self.fig.toolbar.active_scroll = wheel_zoom

        # If not ColumnDataSource exists, then create
        if not self.ColumnDataSource:
            self.create_ColumnDataSource()

        # Create figure
        self.fig_multi = self.fig.multi_line(xs='xs', ys='ys', line_color='line_color', source=self.ColumnDataSource, legend="Contours")
        # Possible for text: angle, angle_units, js_event_callbacks, js_property_callbacks, name,
        # subscribed_events, tags, text, text_align, text_alpha, text_baseline, text_color, text_font, text_font_size,
        # text_font_style, x, x_offset, y or y_offset
        #fig.text(x='xt',y='yt',text='text', source=self.ColumnDataSourceText,
        #    text_baseline='middle', text_align='center', text_font_size="10px", legend="Text")

        # Hide glyphs in Interactive Legends
        self.fig.legend.click_policy="hide" # "mute"

        # Set label
        self.fig.xaxis.axis_label = self.udic[1]['label'] + ' ppm'
        self.fig.yaxis.axis_label = self.udic[0]['label'] + ' ppm'

        return self.fig

    def get_contour_widget(self):
        import ipywidgets as widgets

        # Make widgets
        w_label = widgets.Label(value="Settings for contour:")

        w_contour_start = widgets.FloatText(value=self.contour_start, description='start:')
        w_contour_start.observe(self.change_contour_start_w, names='value')

        w_contour_num = widgets.IntText(value=self.contour_num, description='num:')
        w_contour_num.observe(self.change_contour_num_w, names='value')

        w_contour_factor = widgets.FloatText(value=self.contour_factor, description='factor:')
        w_contour_factor.observe(self.change_contour_factor_w, names='value')

        # Put next to each other
        w_contour = widgets.HBox([w_contour_start, w_contour_num, w_contour_factor])
        # Put on top of each Other
        w_label_contour = widgets.VBox([w_label, w_contour])

        return w_label_contour

    def get_peakpick(self, pthres=None, **kwargs):
        import pandas as pd

        if pthres == None:
            pthres = self.contour_start

        # peak pick the data, return numpy rec.array
        peaks = ng.peakpick.pick(self.data, pthres=pthres, **kwargs)

        # Convert from point position to ppm
        peak_locations_x_ppm = self.x_ppm_scale[peaks['X_AXIS'].astype(int)]
        peak_locations_y_ppm = self.y_ppm_scale[peaks['Y_AXIS'].astype(int)]
        peak_amplitudes = self.data[peaks['Y_AXIS'].astype('int'), peaks['X_AXIS'].astype('int')]

        # Make dict, to pandas
        cols = {'x_ppm': peak_locations_x_ppm,
                'y_ppm': peak_locations_y_ppm,
                'x_p': peaks['X_AXIS'].astype(int),
                'y_p': peaks['Y_AXIS'].astype(int),
                'cID': peaks['cID'].astype(int),
                'VOL': peaks['VOL'],
                'zs': peak_amplitudes
                }
        # Make pandas
        df = pd.DataFrame.from_dict(cols)
        # Rearrange
        df = df[['x_ppm', 'y_ppm', 'x_p', 'y_p', 'cID', 'VOL', 'zs']]

        # Plot
        if hasattr(self, 'fig'):
            # Make datasource
            source = bm.ColumnDataSource(df)
            # And plot
            self.fig_peaks = self.fig.cross(x='x_ppm', y='y_ppm', source=source, size=20, color="#E6550D", line_width=2, legend="Peaks")

        return df
