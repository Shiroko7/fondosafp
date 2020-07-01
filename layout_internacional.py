
import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date


#dataset
df_inter = query_by_daterange("inversion_internacional",start_date,end_date).dropna()

#layout inversiones afp extranjeras
fig_inv_ex = plots.fig_inversiones(df_inter,'INVERSIÓN EXTRANJERA','MMUSD')
fig_inv_ex_rv = plots.fig_inversiones(df_inter,'RENTA FIJA','MMUSD')
fig_inv_ex_rf = plots.fig_inversiones(df_inter,'RENTA VARIABLE','MMUSD')

layout_internacional = html.Div([
    layout_header,
    html.H3('Inversión Internacional'),
    html.Div(
        [
            dcc.Checklist(id='check_fig-ex', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-ex", children=[dcc.Graph(id='fig-ex',figure = fig_inv_ex)],type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Checklist(id='check_fig-ex_rv', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-ex_rv", children=[dcc.Graph(id='fig-ex_rv',figure = fig_inv_ex_rv)],type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Checklist(id='check_fig-ex_rf', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-ex_rf", children=[dcc.Graph(id='fig-ex_rf',figure = fig_inv_ex_rf)],type="circle"),
        ], className='pretty_container'
    ),

])