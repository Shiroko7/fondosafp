

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header, start_date, end_date


layout_inversiones = html.Div([
    layout_header,
    html.H3('Inversiones'),
    html.Div(
        [
            html.P('Intervalo de fechas.'),
            dcc.DatePickerRange(
                id='daterange_inversiones',
                first_day_of_week=1,
                min_date_allowed=datetime(2016, 1, 1),
                max_date_allowed=end_date,
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Loading(id="loading-icon_fig-inv_total",
                        children=[dcc.Graph(id='fig_inv_total')], type="circle"),
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
            dcc.Loading(id="loading-icon_bar-inver",
                        children=[dcc.Graph(id='fig_bar_inver')], type="circle"),
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
            dcc.Loading(id="loading-icon_bar-nacio",
                        children=[dcc.Graph(id='fig_bar_nacio')], type="circle"),
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
            dcc.Loading(id="loading-icon_bar-inter",
                        children=[dcc.Graph(id='fig_bar_inter')], type="circle"),
        ], className='pretty_container'
    ),
])
