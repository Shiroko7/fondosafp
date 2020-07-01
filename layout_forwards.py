

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date


#dataframes
df_fn = query_by_daterange("forwards_nacionales",start_date,end_date).dropna()

df_vf = query_by_daterange("valor_fondos",start_date,end_date).dropna()
df_vf = df_vf[(df_vf != 0).all(1)]
df_q = query_by_daterange("q_index",start_date,end_date).dropna()
df_q = df_q[(df_q != 0).all(1)]

usdclp = query_by_daterange("usdclp",start_date,end_date).dropna() 

df_total = query_by_daterange("inversion_total",start_date,end_date).dropna()
df_nacio = query_by_daterange("inversion_nacional",start_date,end_date).dropna()
df_inter = query_by_daterange("inversion_internacional",start_date,end_date).dropna()


#layout forwards nacionales
fig_fn = plots.fig_forwards_nacional(df_fn,usdclp,df_vf,df_q)
fig_afp = plots.fig_afp(df_vf,usdclp)

bar_nacio = plots.bar_inversion_nacional(df_nacio,'TOTAL')
bar_inter = plots.bar_inversion_internacional(df_inter,'TOTAL')
bar_inver = plots.bar_inversion(df_nacio,df_inter,'TOTAL')

fig_inv_total = plots.fig_inversiones(df_total,'TOTAL ACTIVOS','MMUSD')

fig_inter_hedge = plots.fig_hedge(df_inter,df_fn)

fig_fn_afp = plots.fig_forwards_nacional_afp(df_fn,usdclp,df_vf,df_q)



layout_datos = html.Div([
    layout_header,
    html.H3('Forwards Nacionales'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fn", children=[dcc.Graph(id='fig_fn',figure = fig_fn)],type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_afp", children=[dcc.Graph(id='fig_afp',figure = fig_afp)],type="circle"),
        ], className='pretty_container'
    ),


    html.Div(
        [
            dcc.Loading(id = "loading-icon_fig-inter_hedge", children=[dcc.Graph(id='fig-inter_hedge',figure = fig_inter_hedge)],type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Inversiones'),

    html.Div(
        [
            dcc.Loading(id = "loading-icon_fig-inv_total", children=[dcc.Graph(id='fig-inv_total',figure = fig_inv_total)],type="circle"),  
        ], className='pretty_container'
    ),
    
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_bar-inver",
                options=[
                    {'label': 'Total', 'value': 'TOTAL'},
                    {'label': 'Fondo A', 'value': 'A'},
                    {'label': 'Fondo B', 'value': 'B'},
                    {'label': 'Fondo C', 'value': 'C'},
                    {'label': 'Fondo D', 'value': 'D'},
                    {'label': 'Fondo E', 'value': 'E'},
                ],
                value='TOTAL',
                className="dcc_control no-print"
            ),
            dcc.Loading(id = "loading-icon_bar-inver", children=[dcc.Graph(id='fig_bar-inver',figure = bar_inver)],type="circle"),    
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_bar-nacio",
                options=[
                    {'label': 'Total', 'value': 'TOTAL'},
                    {'label': 'Fondo A', 'value': 'A'},
                    {'label': 'Fondo B', 'value': 'B'},
                    {'label': 'Fondo C', 'value': 'C'},
                    {'label': 'Fondo D', 'value': 'D'},
                    {'label': 'Fondo E', 'value': 'E'},
                ],
                value='TOTAL',
                className="dcc_control no-print"
            ),
            dcc.Loading(id = "loading-icon_bar-nacio", children=[dcc.Graph(id='fig_bar-nacio',figure = bar_nacio)],type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_bar-inter",
                options=[
                    {'label': 'Total', 'value': 'TOTAL'},
                    {'label': 'Fondo A', 'value': 'A'},
                    {'label': 'Fondo B', 'value': 'B'},
                    {'label': 'Fondo C', 'value': 'C'},
                    {'label': 'Fondo D', 'value': 'D'},
                    {'label': 'Fondo E', 'value': 'E'},
                ],
                value='TOTAL',
                className="dcc_control no-print"
            ),
            dcc.Loading(id = "loading-icon_bar-inter", children=[dcc.Graph(id='fig_bar-inter',figure = bar_inter)],type="circle"),  
        ], className='pretty_container'
    ),

    html.H3('Forwards Nacionales + Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fn-afp", children=[dcc.Graph(id='fig_fn_afp',figure = fig_fn_afp)],type="circle"),
        ], className='pretty_container'
    ),
    
])