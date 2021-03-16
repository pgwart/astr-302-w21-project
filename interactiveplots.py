###  This module queries the SDSS data set to generate a scatter plot and Hess diagram.
### The query finds all stars with g - r between -0.5 and 2.5 and g between 14 and 24
### within a radius (in arcminutes) of a given RA and dec (in degrees).
###
###  To use, import into a Jupyter notebook and call the plots() function,
### then specify parameters with widgets.

import matplotlib.pyplot as plt
import numpy as np
from astroquery.sdss import SDSS
from ipywidgets import interactive_output, IntSlider, FloatSlider, Layout, Text, jslink, GridBox, Dropdown, Button, FloatText
#import pandas as pd

def res(ra, dec, ang):
    """Fetches SDSS data with GetNearbyObj function and given parameters"""
    query = """
        SELECT
            s.ra, s.dec,
            s.dered_g as g, s.dered_r as r,
            s.err_g, s.err_r,
            s.flags
  
        FROM
            dbo.fGetNearbyObjEq({}, {}, {}) AS n
        JOIN Star AS s ON n.objID = s.objID
  
        WHERE
            g - r BETWEEN -0.5 AND 2.5
            AND g BETWEEN 14 and 24
        """.format(ra,dec,ang)
        
    return SDSS.query_sql(query, timeout = 600)

#Create widgets
style = {'description_width': 'initial'}

#Boxes and sliders to control the parameters of the query function
RABox = FloatText(value='229.0128', placeholder='', description='Right ascension (degrees)', style=style, disabled=False, grid_area = 'RABox')
RASlider = FloatSlider(value=229.0128, min=0, max=360, continuous_update = False, grid_area = 'RASlider')

DECBox = FloatText(value='-0.1082', placeholder='', description='Declination (degrees)', style=style, disabled=False, grid_area = 'DECBox')
DECSlider = FloatSlider(value=-0.1082, min=-90, max=90, continuous_update = False, grid_area = 'DECSlider')

radBox = FloatText(value='30', placeholder='', description='Radius (arcminutes)', style=style, disabled=False, grid_area = 'radBox')
radSlider = FloatSlider(value=30, min=1, max=120, step=1, continuous_update = False, grid_area = 'radSlider')

#Slider to control the grid size for the Hess diagram
gridSlider = IntSlider(value=100, min=50, max=300, step=1, description='Grid size', style=style, continuous_update = False, grid_area = 'gridSlider')

#Dropdown menu to select the color map for the Hess diagram
hexDrop = Dropdown(options = ['viridis', 'plasma', 'inferno', 'magma', 'hot', 'winter', 'ocean', 'gray', 'binary'],
                   value = 'viridis',
                   description = 'Hess diagram colormap',
                   style=style,
                   disabled = False,
                   grid_area = 'hexDrop'
                )


#Combine widgets into grid
widgrid = GridBox(children = [RABox, RASlider, gridSlider, DECBox, DECSlider, hexDrop, radBox, radSlider],
                  layout=Layout(
                  width ='1300px',
                  align_items = 'flex-start',
                  grid_template_rows = 'auto auto auto',
                  grid_template_columns = '25% 40% 35%',
                  grid_template_areas = '''
                  "RABox RASlider gridSlider"
                  "DECBox DECSlider hexDrop"
                  "radBox radSlider . "
                  ''')
                 ) 
#Link boxes with sliders
RALink = jslink((RABox, 'value'), (RASlider, 'value'))
DECLink = jslink((DECBox, 'value'), (DECSlider, 'value'))
radLink = jslink((radBox, 'value'), (radSlider, 'value'))

def generate_plots(gsize, ra, dec, ang, style):
    """Generates plots from queried data"""
    r = res(ra, dec, ang)
    
    #Exception handling to prevent empty queries, e.g. unsurveyed areas, from causing an error
    try:
        g, gr = [r['g'], r['g']-r['r']]
        fig, (ax1,ax2) = plt.subplots(1,2, figsize = (20,10))
        ax1.scatter(r['ra'], r['dec'], marker='.', s=0.8)
        ax2.hexbin(gr, g, gridsize = gsize, bins='log', cmap = style)
        plt.ylim(24,14)
        ax1.set_ylabel('Dec')
        ax1.set_xlabel('RA')
        ax2.set_ylabel('G')
        ax2.set_xlabel('G-R')        
    except:
        fig, (ax1,ax2) = plt.subplots(1,2, figsize = (20,10))
        
    return

def plots():
    """Displays widgets and plots"""
    out = interactive_output(generate_plots, {'gsize':gridSlider, 'ra':RABox, 'ra':RASlider, 'dec':DECBox, 'dec':DECSlider, 'ang':radBox, 'ang':radSlider, 'style':hexDrop})
    return display(widgrid, out)