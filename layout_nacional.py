

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date

#dataset
df_nacio = query_by_daterange("inversion_nacional",start_date,end_date).dropna()

#layout inversiones afp nacionales
fig_inv_na = plots.fig_inversiones(df_nacio,'INVERSIÓN NACIONAL TOTAL','MMUSD')
fig_inv_na_rv = plots.fig_inversiones(df_nacio,'RENTA VARIABLE','MMUSD')
fig_inv_na_rf = plots.fig_inversiones(df_nacio,'RENTA FIJA','MMUSD')
fig_inv_na_ins = plots.fig_inversiones(df_nacio,'Instrumentos','MMUSD')
fig_inv_na_bb = plots.fig_inversiones(df_nacio,'Bonos Bancarios','MMUSD')
fig_inv_na_dp = plots.fig_inversiones(df_nacio,'Depósitos a Plazo','MMUSD')

layout_nacional = html.Div([
    layout_header,

    html.H3('Inversión Nacional'),
    html.Div(
        [
            dcc.Checklist(id='check_fig-na', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na", children=[dcc.Graph(id='fig-na',figure = fig_inv_na)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rv', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_rv", children=[dcc.Graph(id='fig-na_rv',figure = fig_inv_na_rv)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rf', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_rf", children=[dcc.Graph(id='fig-na_rf',figure = fig_inv_na_rf)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_ins', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_ins", children=[dcc.Graph(id='fig-na_ins',figure = fig_inv_na_ins)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_bb', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_bb", children=[dcc.Graph(id='fig-na_bb',figure = fig_inv_na_bb)],type="circle"),
        ], className='pretty_container'
    ),
    
    html.Div(
        [
            dcc.Checklist(id='check_fig-na_dp', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_dp", children=[dcc.Graph(id='fig-na_dp',figure = fig_inv_na_dp)],type="circle"),
        ], className='pretty_container'
    ),

])