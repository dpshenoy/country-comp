"""
Module for applying plot options
"""

def apply_plot_options(f):
    """
    Input
    -----
        f:  a bokeh.plotting.figure object
    """

    f.xaxis.axis_label_text_font_style = 'normal'
    f.yaxis.axis_label_text_font_style = 'normal'
    f.xaxis.axis_label_text_font_size = '12pt'
    f.yaxis.axis_label_text_font_size = '12pt'

    f.xaxis.major_label_text_font_size = '12pt'
    f.yaxis.major_label_text_font_size = '12pt'

    f.min_border_left = 100
    f.min_border_bottom = 100
