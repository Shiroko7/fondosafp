import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date


df_extranjeros = query_by_daterange("extranjeros",start_date,end_date).dropna()
fig_ex_reg = plots.fig_extranjeros(df_extranjeros)

layout_extranjeros = html.Div([
    layout_header,
    html.H3('Inversión en Regiones'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fig-ex_reg", children=[dcc.Graph(id='fig-ex_reg',figure = fig_ex_reg)],type="circle"),  
        ], className='pretty_container'
    ),

])