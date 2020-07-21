import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header, start_date, end_date

layout_extranjeros = html.Div([
    layout_header,
    html.H3('Inversión en Regiones'),
    html.Div(
        [
            html.P('Intervalo de fechas.'),
            dcc.DatePickerRange(
                id='daterange_extranjeros',
                first_day_of_week=1,
                min_date_allowed=datetime(2016, 1, 1),
                max_date_allowed=end_date,
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Loading(id="loading-icon_fig-ex_reg",
                        children=[dcc.Graph(id='fig_ex_reg')], type="circle"),
        ], className='pretty_container'
    ),

])
