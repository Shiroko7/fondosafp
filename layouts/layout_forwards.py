

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layouts.layout_home import layout_header, start_date, end_date


layout_datos = html.Div([
    layout_header,
    html.H3('Forwards Nacionales'),
    html.Div(
        [
            html.P('Intervalo de fechas.'),
            dcc.DatePickerRange(
                id='daterange_forwards',
                first_day_of_week=1,
                min_date_allowed=datetime(2016, 1, 1),
                max_date_allowed=end_date,
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Loading(id="loading-icon_fn",
                        children=[dcc.Graph(id='fig_fn')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_fig_inter_hedge_total", children=[dcc.Graph(
                id='fig_inter_hedge_total')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_fig_inter_hedge", children=[dcc.Graph(
                id='fig_inter_hedge')], type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id="loading-icon_afp",
                        children=[dcc.Graph(id='fig_afp')], type="circle"),
        ], className='pretty_container'
    ),

    html.H3('Forwards Nacionales + Fondos AFP'),
    html.Div(
        [
            dcc.Loading(id="loading-icon_fn-afp",
                        children=[dcc.Graph(id='fig_fn_afp')], type="circle"),
        ], className='pretty_container'
    ),
            html.Div(
                [
                    html.Div([
                              html.Div([html.P('Fuente: Superintendencia de Pensiones')],
                                       className='Fuente'),
                              html.P('Este archivo es confidencial y destinado únicamente para uso interno.', style={'textAlign': 'right', 'fontStyle': 'italic'
                                                                                                                     }), ], className='twelve columns')
                ],
                className="foot row",
            ),
])
