from plotext._default import default_figure_class
from plotext._monitor import monitor_class
import plotext._utility.doc as doc
import plotext._utility as ut
from time import time
import os

class _figure_class():
    def __init__(self, master = None, parent = None):
        self._set_family(master, parent) 
        self.default = default_figure_class() # default values
        self._time = None # computational time

        self._set_size(None, None) # no initial size
        self._limit_master_size(True, True) if self._is_master else None # limit size initially for master
        self._set_terminal_size(*ut.terminal_size()) if self._is_master else None # get terminal size for master
        self._set_master_size() if self._is_master else None # set master size to terminal
        
        self._set_slots_max(*self._master._size) # sets the maximum number of subplots in the current figure
        self._set_slots(0, 0) # no subplots, the current figure is used as plotting monitor
        self._set_subplots() 
        
        self.monitor = monitor_class() if self._is_master else self._parent.monitor.copy() # each figure has a monitor for plotting; which by default is copied from the parent figure monitor so that all plots can be duplicated in each subplot without rewriting code 
        self.monitor.size = self._size
        self.date = self.monitor.date

        if self._is_master:
            self.dummy = _figure_class(self._master, self._parent) # the master has a dumm container for subplots that do not actually exist (anymore due to change of size) 

    def _set_family(self, master = None, parent = None):
        self._parent = self if parent is None else parent # the figure just above this one
        self._master = self if master is None else master # the figure above all others
        self._is_master = self is self._master
        self._active = self if self._is_master else self._master._active # the active figure
        self._take_max()

    def main(self): # returns the master figure
        self._master._active = self._master
        return self._master

##############################################
###########    Size Functions    #############
##############################################

    def _limit_master_size(self, width = None, height = None):
        self._limit_width = self.default.limit_width if width is None else bool(width)
        self._limit_height = self.default.limit_height if height is None else bool(height)
        self._limit = [self._limit_width, self._limit_height]

    def _set_size(self, width = None, height = None):
        self._width = None if width is None else int(width)
        self._height = None if height is None else int(height)
        self._size = [self._width, self._height]

    def plot_size(self, width = None, height = None):
        width = self._width if width is None else width
        height = self._height if height is None else height
        self._set_size(width, height)
        self._set_master_size() if self._is_master else None
        self.monitor.size = self._size
        
    plotsize = plot_size

    def _set_terminal_size(self, width = None, height = None):
        self._width_term = self.default._width_term if width is None else width
        extra_lines = 2 if ut.is_ipython() else 1
        self._height_term = self.default._height_term if height is None else max(height - extra_lines, 0)
        self._size_term = [self._width_term, self._height_term]

    def _set_master_size(self):
        width = self._width_term if self._width is None or (self._width > self._width_term and self._limit_width) else self._width
        height = self._height_term if self._height is None or (self._height > self._height_term and self._limit_height) else self._height
        self._set_size(width, height)
        
##############################################
#########    Subplots Functions    ###########
##############################################

    def _set_slots_max(self, width = None, height = None):
        self._rows_max = (height + 1) // 3 
        self._cols_max = (width + 1) // 3 
        self._slots_max = [self._rows_max, self._cols_max]

    def _set_slots(self, rows = None, cols = None):
        rows = 1 if rows is None else int(abs(rows))
        cols = 1 if cols is None else int(abs(cols))
        self._rows = min(rows, self._rows_max)
        self._cols = min(cols, self._cols_max)
        self._Rows = list(range(1, self._rows + 1))
        self._Cols = list(range(1, self._cols + 1))
        self._slots = [self._rows, self._cols]
        self._no_plots = 0 in self._slots #or self._is_master

    def _set_subplots(self):
        self.subfig = [[_figure_class(self._master, self._parent) for col in self._Cols] for row in self._Rows]
        
    def subplots(self, rows = None, cols = None):
        self._set_slots(rows, cols)
        self._set_subplots()
        return self

    def _get_subplot(self, row = None, col = None):
        return self.subfig[row - 1][col - 1] if row in self._Rows and col in self._Cols else self._master.dummy

    def subplot(self, row = None, col = None):
        active = self._get_subplot(row, col)
        self._active = active
        self._master._active = active
        return self._master._active

##############################################
#######    External Set Functions    #########
##############################################

    def title(self, title = None):
        self.monitor.set_title(title) if self._no_plots else [[self._get_subplot(row, col).title(title) for col in self._Cols] for row in self._Rows]

    def xlabel(self, label = None, xside = None):
        self.monitor.set_xlabel(label = label, xside = xside) if self._no_plots else [[self._get_subplot(row, col).xlabel(label = label, xside = xside) for col in self._Cols] for row in self._Rows]
        
    def ylabel(self, label = None, yside = None):
        self.monitor.set_ylabel(label = label, yside = yside) if self._no_plots else [[self._get_subplot(row, col).ylabel(label = label, yside = yside) for col in self._Cols] for row in self._Rows]

    def xlim(self, lower = None, upper = None, xside = None):
        self.monitor.set_xlim(lower = lower, upper = upper, xside = xside) if self._no_plots else [[self._get_subplot(row, col).xlim(lower = lower, upper = upper, xside = xside) for col in self._Cols] for row in self._Rows]

    def ylim(self, left = None, right = None, yside = None):
        self.monitor.set_ylim(left = left, right = right, yside = yside) if self._no_plots else [[self._get_subplot(row, col).ylim(left = left, right = right, yside = yside) for col in self._Cols] for row in self._Rows]
        
    def xscale(self, scale = None, xside = None):
        self.monitor.set_xscale(scale = scale, xside = xside) if self._no_plots else [[self._get_subplot(row, col).xscale(scale = scale, xside = xside) for col in self._Cols] for row in self._Rows]
        
    def yscale(self, scale = None, yside = None):
        self.monitor.set_yscale(scale = scale, yside = yside) if self._no_plots else [[self._get_subplot(row, col).yscale(scale = scale, yside = yside) for col in self._Cols] for row in self._Rows]
        
    def xticks(self, ticks = None, labels = None, xside = None):
        self.monitor.set_xticks(ticks = ticks, labels = labels, xside = xside) if self._no_plots else [[self._get_subplot(row, col).xticks(ticks = ticks, labels = labels, xside = xside) for col in self._Cols] for row in self._Rows]

    def yticks(self, ticks = None, labels = None, yside = None):
        self.monitor.set_yticks(ticks = ticks, labels = labels, yside = yside) if self._no_plots else [[self._get_subplot(row, col).yticks(ticks = ticks, labels = labels, yside = yside) for col in self._Cols] for row in self._Rows]

    def xfrequency(self, frequency = None, xside = None):
        self.monitor.set_xfrequency(frequency = frequency, xside = xside) if self._no_plots else [[self._get_subplot(row, col).xfrequency(frequency = frequency, xside = xside) for col in self._Cols] for row in self._Rows]

    def yfrequency(self, frequency = None, yside = None):
        self.monitor.set_yfrequency(frequency = frequency, yside = yside) if self._no_plots else [[self._get_subplot(row, col).yfrequency(frequency = frequency, yside = yside) for col in self._Cols] for row in self._Rows]

    def xaxes(self, lower = None, upper = None):
        self.monitor.set_xaxes(lower = lower, upper = upper) if self._no_plots else [[self._get_subplot(row, col).xaxes(lower = lower, upper = upper) for col in self._Cols] for row in self._Rows]

    def yaxes(self, left = None, right = None):
        self.monitor.set_yaxes(left = left, right = right) if self._no_plots else [[self._get_subplot(row, col).yaxes(left = left, right = right) for col in self._Cols] for row in self._Rows]

    def frame(self, frame = None):
        self.monitor.set_frame(frame = frame) if self._no_plots else [[self._get_subplot(row, col).frame(frame = frame) for col in self._Cols] for row in self._Rows]
        
    def grid(self, horizontal = None, vertical = None):
        self.monitor.set_grid(horizontal = horizontal, vertical = vertical) if self._no_plots else [[self._get_subplot(row, col).grid(horizontal = horizontal, vertical = vertical) for col in self._Cols] for row in self._Rows]

    def canvas_color(self, color = None):
        self.monitor.set_canvas_color(color) if self._no_plots else [[self._get_subplot(row, col).canvas_color(color) for col in self._Cols] for row in self._Rows]

    def axes_color(self, color = None):
        self.monitor.set_axes_color(color) if self._no_plots else [[self._get_subplot(row, col).axes_color(color) for col in self._Cols] for row in self._Rows]

    def ticks_color(self, color = None):
        self.monitor.set_ticks_color(color) if self._no_plots else [[self._get_subplot(row, col).ticks_color(color) for col in self._Cols] for row in self._Rows]
        
    def ticks_style(self, style = None):
        self.monitor.set_ticks_style(style) if self._no_plots else [[self._get_subplot(row, col).ticks_style(style) for col in self._Cols] for row in self._Rows]
        
    def theme(self, theme = None):
        self.monitor.set_theme(theme) if self._no_plots else [[self._get_subplot(row, col).theme(theme) for col in self._Cols] for row in self._Rows]

##############################################
###########    Clear Functions    ############
###########################x##################

    def clear_figure(self):
        self.__init__()# if self._no_plots else [[self._get_subplot(row, col).clear_figure() for col in self._Cols] for row in self._Rows]
    clf = clear_figure
    
    def clear_data(self):
        self.monitor.data_init() if self._no_plots else [[self._get_subplot(row, col).clear_data() for col in self._Cols] for row in self._Rows]
    cld = clear_data

    def clear_color(self):
        self.monitor.clear_color() if self._no_plots else [[self._get_subplot(row, col).clear_color() for col in self._Cols] for row in self._Rows]
    clc = clear_color

##############################################
###########    Plot Functions    #############
##############################################

    def _draw(self, *args, **kwargs):
        self.monitor.draw(*args, **kwargs) if self._no_plots else [[self._get_subplot(row, col)._draw(*args, **kwargs) for col in self._Cols] for row in self._Rows]

    def scatter(self, *args, xside = None, yside = None, marker = None, color = None, style = None, fillx = None, filly = None, label = None):
        self._draw(*args, xside = xside, yside = yside, lines = False, marker = marker, color = color, style = style, fillx = fillx, filly = filly, label = label)

    def plot(self, *args, xside = None, yside = None, marker = None, color = None, style = None, fillx = None, filly = None, label = None):
        self._draw(*args, xside = xside, yside = yside, lines = True, marker = marker, color = color,  fillx = fillx, filly = filly, label = label)
        
    def error(self, *args, xerr = None, yerr = None, xside = None, yside = None, color = None, label = None):
        self.monitor.draw_error(*args, xerr = xerr, yerr = yerr, xside = xside, yside = yside, color = color, label = label)

    def candlestick(self, dates, data, orientation = None, colors = None, label = None):
        self.monitor.draw_candlestick(dates, data, orientation = orientation, colors = colors, label = label) if self._no_plots else [[self._get_subplot(row, col).candlestick(dates, data, orientation = orientation, colors = colors, label = label) for col in self._Cols] for row in self._Rows]

    def bar(self, *args, xside = None, yside = None, marker = None, color = None, fill = None, width = None, orientation = None, label = None, minimum = None):
        self.monitor.draw_bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) if self._no_plots else [[self._get_subplot(row, col).bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) for col in self._Cols] for row in self._Rows]
    
    def multiple_bar(self, *args, xside = None, yside = None, marker = None, color = None, fill = None, width = None, orientation = None, label = None, minimum = None):
        self.monitor.draw_multiple_bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) if self._no_plots else [[self._get_subplot(row, col).multiple_bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) for col in self._Cols] for row in self._Rows]
    
    def stacked_bar(self, *args, xside = None, yside = None, marker = None, color = None, fill = None, width = None, orientation = None, label = None, minimum = None):
        self.monitor.draw_stacked_bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) if self._no_plots else [[self._get_subplot(row, col).stacked_bar(*args, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) for col in self._Cols] for row in self._Rows]

    def hist(self, data, bins = None, norm = None, xside = None, yside = None, marker = None, color = None, fill = None, width = None, orientation = None, label = None, minimum = None):
        self.monitor.draw_hist(data, bins = bins, norm = norm, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) if self._no_plots else [[self._get_subplot(row, col).hist(data, bins = bins, norm = norm, xside = xside, yside = yside, marker = marker, color = color, fill = fill, width = width, orientation = orientation, label = label, minimum = minimum) for col in self._Cols] for row in self._Rows]

    def matrix_plot(self, matrix, marker = None, style = None, fast = False):
        self.monitor.draw_matrix(matrix, marker = marker, style = style, fast = fast) if self._no_plots else [[self._get_subplot(row, col).matrix_plot(matrix, marker = marker, style = style, fast = fast) for col in self._Cols] for row in self._Rows]
    
    def image_plot(self, path, marker = None, style = None, grayscale = False, fast = False):
        self.monitor.draw_image(path, marker = marker, style = style, grayscale = grayscale, fast = fast) if self._no_plots else [[self._get_subplot(row, col).image_plot(path, marker = marker, style = style, grayscale = grayscale, fast = fast) for col in self._Cols] for row in self._Rows]

##############################################
###########    Plotting Tools    #############
##############################################

    def event_plot(self, data, orientation = None, marker = None, color = None, side = None):
        self.monitor.draw_event_plot(data, orientation = orientation, marker = marker, color = color, side = side) if self._no_plots else [[self._get_subplot(row, col).event_plot(data, orientation = orientation, marker = marker, color = color, side = side) for col in self._Cols] for row in self._Rows]
    eventplot = event_plot

    def vertical_line(self, coordinate, color = None, xside = None):
        self.monitor.draw_vertical_line(coordinate, color = color, xside = xside) if self._no_plots else [[self._get_subplot(row, col).vertical_line(coordinate, color = color, xside = xside) for col in self._Cols] for row in self._Rows]
    vline = vertical_line
        
    def horizontal_line(self, coordinate, color = None, yside = None):
        self.monitor.draw_horizontal_line(coordinate, color = color, yside = yside) if self._no_plots else [[self._get_subplot(row, col).horizontal_line(coordinate, color = color, yside = yside) for col in self._Cols] for row in self._Rows]     
    hline = horizontal_line

    def text(self, text, x, y, xside = None, yside = None, color = None, style = None, alignment = None):
        self.monitor.draw_text(text, x, y, xside = xside, yside = yside, color = color, style = style, alignment = alignment) if self._no_plots else [[self._get_subplot(row, col).text(text, x, y, xside = xside, yside = yside, color = color, style = style, alignment = alignment) for col in self._Cols] for row in self._Rows]

##############################################
###########    Build Functions    ############
##############################################

    def show(self): # it shows the current figure
        t = time()
        self.build()
        ut.write(self.monitor.canvas)
        self._time = time() - t
        self.main()

    def build(self): # it build the current figure without showing it
        self._set_sizes()
        self._build_matrix()
        self.monitor.to_canvas()
        return self.monitor.canvas

    def _get_time(self, show = True): # it returns the computational time of latest show or build function
        if show:
            print(ut.format_time("plotext time", self._time))
        return self._time

    def save_fig(self, path = None, keep_colors = False): # it saves the plot as text or html, keep_colors = True preserves ansi colors for texts
        path = 'plotext.txt' if path is None or not ut.correct_path(path) else path
        _, extension = os.path.splitext(path)
        text = self.monitor.canvas
        if extension == ".html":
            text = self.monitor.to_html()
        elif not keep_colors:
            text = ut.uncolorize(self.monitor.canvas)
        ut.save_text(text, path)
    savefig = save_fig

##############################################
###########    Build Utilities    ############
##############################################

    def _build_matrix(self):
        if self._no_plots:
            self.monitor.build_plot(*self._size) if not self.monitor.fast_plot else None
        else:
            [[self._get_subplot(row, col)._build_matrix() for col in self._Cols] for row in self._Rows]
            m = [[self._get_subplot(row, col).monitor.matrix for col in self._Cols] for row in self._Rows]
            self.monitor.matrix = m = ut.join_matrices(m)

    def _take_max(self): # in a matrix of subplots the maximum height/width is considered (by default) for each row/column
        self.max_or_min = max
        
    def take_min(self): # in a matrix of subplots the maximum height/width will be considered for each row/column
        self.max_or_min = min

    def _get_widths(self): # the subplots max/min widths for each column
        widths = [[self._get_subplot(row, col)._width for row in self._Rows] for col in self._Cols]
        widths = [self.max_or_min([sub for sub in el if sub is not None], default = None) for el in widths]
        return widths

    def _get_heights(self): # the subplots max/min heights for each row
        heights = [[self._get_subplot(row, col)._height for col in self._Cols] for row in self._Rows]
        heights = [self.max_or_min([sub for sub in el if sub is not None], default = None) for el in heights]
        return heights

    def _set_subplot_size(self, row = None, col = None, width = None, height = None):
        self._get_subplot(row, col)._set_size(width, height)
        self._get_subplot(row, col)._set_sizes() #if not self._no_plots else None

    def _set_sizes(self):
        self._set_slots_max(*self._size)
        self._set_slots(*self._slots)
        widths = self._get_widths()
        widths = set_sizes(widths, self._width) # it sets the free subplots widths in accord with the parent figure width 
        widths = fit_sizes(widths, self._width) # it fits the subplots widths to the parent figure width 
        heights = self._get_heights()
        heights = set_sizes(heights, self._height) # it sets the free subplots height in accord with the parent figure height 
        heights = fit_sizes(heights, self._height) # it fits the subplots heights to the parent figure height
        width = sum(widths) if len(widths) > 1 else self._width
        height = sum(heights) if len(widths) > 1 else self._height
        #self._set_size(width, height)
        [[self._set_subplot_size(row, col, widths[col - 1], heights[row - 1]) for col in self._Cols] for row in self._Rows] if (not self._no_plots) else None
        
##############################################
###########    Date Functions    #############
##############################################

    def date_form(self, input_form = None, output_form = None):
        self._master.dummy.date.date_form(input_form, output_form)
        if self._no_plots:
            self.monitor.date.date_form(input_form, output_form)
        else:
            [[self._get_subplot(row, col).date_form(input_form, output_form) for col in self._Cols] for row in self._Rows]
        
    def set_time0(self, string, form = None):
        self.monitor.date.set_time0(string, form) if self._no_plots else [[self._get_subplot(row, col).set_time0(string, form) for col in self._Cols] for row in self._Rows]

    def today_datetime(self):
        return self.monitor.date.today_datetime()
    
    def today_string(self, output_form = None):
        return self.monitor.date.today_string(output_form)
    
    def datetime_to_string(self, datetime, output_form = None):
        return self.monitor.date.datetime_to_string(datetime, output_form = output_form)
    
    def datetimes_to_string(self, datetimes, output_form = None):
        return self.monitor.date.datetimes_to_string(datetimes, output_form = output_form)
        
    def string_to_datetime(self, string, input_form = None):
        return self.monitor.date.string_to_datetime(string, input_form = input_form)
    
    def string_to_time(self, string, input_form = None):
        return self.monitor.date.string_to_time(string, input_form = input_form)
    
    def strings_to_time(self, string, input_form = None):
        return self.monitor.date.strings_to_time(string, input_form = input_form)

##############################################
############     Docstrings    ###############
##############################################

    subplots.__doc__ = doc._subplots
    subplot.__doc__ = doc._subplot
    main.__doc__ = doc._main
    
    plot_size.__doc__ = doc._plot_size
    take_min.__doc__ = doc._take_min
    
    title.__doc__ = doc._title
    xlabel.__doc__ = doc._xlabel
    ylabel.__doc__ = doc._ylabel
    xlim.__doc__ = doc._xlim
    ylim.__doc__ = doc._ylim
    xscale.__doc__ = doc._xscale
    yscale.__doc__ = doc._yscale
    xticks.__doc__ = doc._xticks
    yticks.__doc__ = doc._yticks
    xfrequency.__doc__ = doc._xfrequency
    yfrequency.__doc__ = doc._yfrequency
    xaxes.__doc__ = doc._xaxes
    yaxes.__doc__ = doc._yaxes
    frame.__doc__ = doc._frame
    grid.__doc__ = doc._grid
    canvas_color.__doc__ = doc._canvas_color
    axes_color.__doc__ = doc._axes_color
    ticks_color.__doc__ = doc._ticks_color
    ticks_style.__doc__ = doc._ticks_style
    theme.__doc__ = doc._theme
    
    clear_figure.__doc__ = doc._clear_figure
    clear_data.__doc__ = doc._clear_data
    clear_color.__doc__ = doc._clear_color
    
    scatter.__doc__ = doc._scatter
    plot.__doc__ = doc._plot
    candlestick.__doc__ = doc._candlestick
    bar.__doc__ = doc._bar
    multiple_bar.__doc__ = doc._multiple_bar
    stacked_bar.__doc__ = doc._stacked_bar
    hist.__doc__ = doc._hist
    matrix_plot.__doc__ = doc._matrix_plot
    image_plot.__doc__ = doc._image_plot
    
    event_plot.__doc__ = doc._event_plot
    vertical_line.__doc__ = doc._vertical_line
    horizontal_line.__doc__ = doc._horizontal_line
    text.__doc__ = doc._text
    
    show.__doc__ = doc._show
    build.__doc__ = doc._build
    save_fig.__doc__ = doc._save_fig
    
    date_form.__doc__ = doc._date_form
    set_time0.__doc__ = doc._set_time0
    today_datetime.__doc__ = doc._today_datetime
    today_string.__doc__ = doc._today_string
    datetime_to_string.__doc__ = doc._datetime_to_string
    datetimes_to_string.__doc__ = doc._datetimes_to_string
    string_to_datetime.__doc__ = doc._string_to_datetime
    
##############################################
#########    Utility Functions    ############
##############################################

def set_sizes(sizes, size_max):
    bins = len(sizes)
    for s in range(bins):
        size_set = sum([el for el in sizes[0 : s] + sizes[s + 1 : ] if el is not None])
        available = max(size_max - size_set, 0)
        to_set = len([el for el in sizes[s : ] if el is None])
        sizes[s] = available // to_set if sizes[s] is None else sizes[s]
    return sizes

def fit_sizes(sizes, size_max): 
    bins = len(sizes)
    s = bins - 1
    #while (sum(sizes) != size_max if not_less else sum(sizes) > size_max) and s >= 0:
    while sum(sizes) > size_max and s >= 0:
        other_sizes = sum([sizes[i] for i in range(bins) if i != s])
        sizes[s] = max(size_max - other_sizes, 0)
        s -= 1
    return sizes


