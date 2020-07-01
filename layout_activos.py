
import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header,start_date,end_date


#dataset
df_activos = query_by_daterange("activos",start_date,end_date).dropna()

#layout activos de pensiones
fig_act_bclp = plots.fig_activos(df_activos,'Bonos CLP','porcentaje')
fig_act_buf = plots.fig_activos(df_activos,'Bonos UF','porcentaje')
fig_act_ex = plots.fig_activos(df_activos,'TOTAL EXTRANJERO','porcentaje')



layout_activos = html.Div([
    layout_header,
    html.H3('Activos de Pensiones'),
    html.Div(
        [            
            dcc.Loading(id = "loading-icon_fig-act_bclp", children=[dcc.Graph(id='fig-act_bclp',figure = fig_act_bclp)],type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [            
            dcc.Loading(id = "loading-icon_fig-act_buf", children=[dcc.Graph(id='fig-act_buf',figure = fig_act_buf)],type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [            
            dcc.Loading(id = "loading-icon_fig-act_ex", children=[dcc.Graph(id='fig-act_ex',figure = fig_act_ex)],type="circle"),
        ], className='pretty_container'
    ),
])