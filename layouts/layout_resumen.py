import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

end_date = date.today()  # - timedelta(date.today().day)
start_date = end_date - timedelta(days=2*365)

layout_resumen = html.Div([
    html.P('Intervalo de fechas.'),
    dcc.DatePickerRange(
        id='daterange_resumen',
        first_day_of_week=1,
        min_date_allowed=datetime(2016, 1, 1),
        max_date_allowed=end_date,
        initial_visible_month=end_date-timedelta(days=3*30),
        minimum_nights=60,
        start_date=start_date,
        end_date=end_date,
        display_format='M-D-Y',
    ),
    html.Div(
        [
            html.Div(
                [
                    html.H2('Resumen Carteras AFPs',),
                ], className='twelve columns', style={'text-align': 'center'}
            )
        ], className='twelve columns',
    ),
    html.H4('Activos administrtivos'),
    html.Div(
        [
            dcc.Loading(id="loading_patrimonio_ajustado_total", children=[dcc.Graph(
                id='fig_patrimonio_ajustado_total')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_patrimonio_ajustado_afps", children=[dcc.Graph(
                id='fig_patrimonio_ajustado_afps')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inversiones_total", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_total')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inter_hedge_total", children=[dcc.Graph(
                id='fig_patrimonio_inter_hedge_total')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inter_hedge", children=[dcc.Graph(
                id='fig_patrimonio_inter_hedge')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inversiones_nacional", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_nacional')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Loading(id="loading_inversiones_nacional_monedas", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_nacional_monedas')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Loading(id="loading_inversiones_internacional", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_internacional')], type="circle"),
        ], className='pretty_container'
    ),
    html.H4('Inversión Internacional'),
    html.Div(
        [
            dcc.Loading(id="loading_extranjeros_total", children=[dcc.Graph(
                id='fig_patrimonio_extranjeros_total')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_extranjeros_fondos", children=[dcc.Graph(
                id='fig_patrimonio_extranjeros_fondos')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_forwards_n", children=[dcc.Graph(
                id='fig_patrimonio_forwards_n')], type="circle"),
        ], className='pretty_container'
    ),
])
