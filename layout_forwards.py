

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date


#dataframes
df_fn = query_by_daterange("forwards_nacionales",start_date,end_date).dropna()
df_fn = df_fn.sort_values(by = 'Fecha')
df_fn.reset_index(inplace=True,drop=True)
dfc = df_fn[df_fn['Nombre'] == 'Compra']
dfv = df_fn[df_fn['Nombre'] == 'Venta']

df_vf = query_by_daterange("valor_fondos",start_date,end_date).dropna()
df_vf = df_vf[(df_vf != 0).all(1)]
df_vf = df_vf.sort_values(by = 'Fecha')
df_vf.reset_index(inplace=True,drop=True)


df_q = query_by_daterange("q_index",start_date,end_date).dropna()
df_q = df_q[(df_q != 0).all(1)]
df_q = df_q.sort_values(by = 'Fecha')
df_q.reset_index(inplace=True,drop=True)

usdclp = query_by_daterange("usdclp",start_date,end_date).dropna() 

df_inter = query_by_daterange("inversion_internacional",start_date,end_date).dropna()

#layout forwards nacionales
fig_fn = plots.fig_forwards_nacional(dfc,dfv,df_fn,usdclp,df_vf,df_q)
fig_afp = plots.fig_afp(df_vf,usdclp)

fig_fn_afp = plots.fig_forwards_nacional_afp(dfc,dfv,df_fn,usdclp,df_vf,df_q)


fig_inter_hedge = plots.fig_hedge(df_inter,dfc,dfv,df_fn)

layout_datos = html.Div([
    layout_header,
    html.H3('Forwards Nacionales'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fn", children=[dcc.Graph(id='fig_fn',figure = fig_fn)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Loading(id = "loading-icon_fig-inter_hedge", children=[dcc.Graph(id='fig-inter_hedge',figure = fig_inter_hedge)],type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_afp", children=[dcc.Graph(id='fig_afp',figure = fig_afp)],type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Forwards Nacionales + Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fn-afp", children=[dcc.Graph(id='fig_fn_afp',figure = fig_fn_afp)],type="circle"),
        ], className='pretty_container'
    ),
    
])