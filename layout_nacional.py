

import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

from layout_home import layout_header, start_date, end_date


layout_nacional = html.Div([
    layout_header,

    html.H3('Inversión Nacional'),
    html.Div([
        html.P('Intervalo de fechas.'),
        dcc.DatePickerRange(
            id='daterange_nacional',
            first_day_of_week=1,
            min_date_allowed=datetime(2016, 1, 1),
            max_date_allowed=end_date,
            initial_visible_month=end_date,
            start_date=start_date,
            end_date=end_date,
            display_format='M-D-Y',
        ),
        dcc.Checklist(id='check_fig-na', options=[
            {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
        dcc.Loading(id="loading-icon_fig-na",
                    children=[dcc.Graph(id='fig_na')], type="circle"),
    ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rv', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_fig-na_rv", children=[dcc.Graph(
                id='fig_na_rv')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rf', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_fig-na_rf", children=[dcc.Graph(
                id='fig_na_rf')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_ins', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_fig-na_ins", children=[dcc.Graph(
                id='fig_na_ins')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_bb', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_fig-na_bb", children=[dcc.Graph(
                id='fig_na_bb')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_dp', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_fig-na_dp", children=[dcc.Graph(
                id='fig_na_dp')], type="circle"),
        ], className='pretty_container'
    ),

])
