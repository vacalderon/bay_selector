#*******************************************************
#*******************************************************
#****       BAY SELECTOR APP                        ****
#****                                               ****
#****       Developed: Victor A. Calderon, PhD, PE  ****
#****                  Murat Melek, PhD, PE         ****
#****                                               ****
#****       Walter P. Moore (c) 2023                ****
#****                                               ****
#****                                               ****
#*******************************************************
#*******************************************************

# Data can be filtered according to the following criteria:
# * Floor Type
# * Girder Span
# * Beam Span
# * Generate a new table to select girder and beam. In each cell the information included is:
#   Girder Section, Beam Section; Girder Camber, Beam Bamber; Girder Studs, Beam Studs; 
#   Beam spacing; Total Unit Carbon, Cost and Weight.

# IMPORTS

import pandas as pd
import streamlit as st
import math as math
from bokeh.plotting import figure
from bokeh.models import Label

# BAY SELECTION DATABASE

bay_db = pd.read_csv('results.csv')
# Converting column names to lowercase and spaces changed to lower hyphen _
bay_db.columns=bay_db.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# INPUTS FROM USER 

st.title('Project Lightning Bay Selector')

deck_select = st.selectbox('Select Deck Type',('3" Deck with 4.50" NW topping concrete', '3" Deck with 3.50" NW topping concrete', '3" Deck with 2.00" NW topping concrete', '3" Deck with 3.25" LW topping concrete', '3" Deck with 2.50" LW topping concrete', '3" Deck with 2.00" LW topping concrete', '2" Deck with 4.50" NW topping concrete', '2" Deck with 3.50" NW topping concrete', '2" Deck with 2.00" NW topping concrete', '2" Deck with 3.25" LW topping concrete', '2" Deck with 2.50" LW topping concrete', '2" Deck with 2.00" LW topping concrete'))
deflection_limit =  st.selectbox('Deflection Limit', ('L/240', 'L/480'))
designpriority =  st.selectbox('Design Priority', ("EmbodiedCarbon", "Cost", "Tonnage"))
girder_span_select = st.slider('Girder Span', 20, 50, 30, 5)
beam_span_select = st.slider('Beam Span', 20, 50, 30, 5)
max_depth_select = st.slider('max depth', 24,48,24,6)

# SETTING UP FILTERS

deck = 'W' + deck_select[0] + '_'+deck_select[13:17]+'_'+ deck_select[19:21]+'_20g'
deck_filter = (bay_db.deck_type == deck)
girder_filter = (bay_db.girder_span == girder_span_select)
depth_filter = (bay_db.max_girder_depth == max_depth_select)
beam_filter = (bay_db.beam_span == beam_span_select)
design_filter = (bay_db.design_priority == designpriority)
deflection_filter = (bay_db.deflection == deflection_limit)
all_filters=deck_filter & girder_filter & depth_filter & beam_filter & design_filter & deflection_filter
bay_filtered = bay_db[all_filters]

girder_section = bay_filtered.girder_section.to_string()[4:]
beam_section = bay_filtered.beam_section.to_string()[4:]
beam_spacing = bay_filtered.beam_spacing_ft.to_string()[5:]
n_beams = round(girder_span_select/float(beam_spacing)) + 1

# OUTPUT RESULTS

st.subheader('Girder and beam section for a '+ str(girder_span_select) + '\' x ' + str(beam_span_select)+'\' bay')
st.write('The most efficient sections for this bay for the selected parameters are:')
st.write('Girder: ', girder_section)
st.write('Beam: ', beam_section)

# Draw bay sketch

p = figure(width=400, height=400)

for i in range(0,n_beams):
    x = [i*float(beam_spacing),i*float(beam_spacing)]
    y = [0,float(beam_span_select)]

    color = '#990000'
    p.line(x, y, line_width=2, color=color)
    p.add_layout(Label(text=beam_section, x=x[0], y=y[1]*0.5-2.5,angle=math.radians(90)))

for i in range (0,2):
    x = [0,float(girder_span_select)]
    y = [i*float(beam_span_select),i*float(beam_span_select)]
    color = '#545066'
    p.line(x, y, line_width=4, color=color)
    p.add_layout(Label(text=girder_section, x=x[1]*0.5-2.5, y=y[0],angle=math.radians(0)))

st.bokeh_chart(p, use_container_width=True)