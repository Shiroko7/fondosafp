import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

start_date = date(2016,1,1)

today = date.today()

#last update info
confirmado, disponible = fetch_last_update(today)
end_date = pd.to_datetime(disponible, format="%d-%b-%Y")

#layout vfs
#fig_vf = plots.fig_valor_fondos(df_vf)
#fig_q = plots.fig_q_index(df_q)

header = html.Div(
            [
                html.Div(
                    [
                        html.H2('AFP Data',),
                        html.H6('Versión Beta 2.0.1',className='no-print'),
                    ],className='nine columns',style = {'text-align': 'center', 'margin-right': '16.6%'}
                )
            ],className='nine columns',
        )


links = html.Div(
    [
        html.Ul(
            [
                html.Li([dcc.Link('Forward Nacionales', href='/apps/datos-principales'),]),
                html.Li([dcc.Link('Inversiones', href='/apps/inversiones'),]),
                html.Li([dcc.Link('Inversión Nacional', href='/apps/inversion-nacional'),]),
                html.Li([dcc.Link('Inversión Internacional', href='/apps/inversion-internacional'),]),
                html.Li([dcc.Link('Activos de Pensiones', href='/apps/activos'),]),
                #html.Li([dcc.Link('Valores Fondos', href='/apps/valores'),]),
                html.Li([dcc.Link('Inversión en Regiones', href='/apps/extranjeros'),]),
            ]
        ), 
    ],className="pretty_container three columns"
)


layout_header = html.Div([
    links,
    header,
],className="row")

layout_home = html.Div([
    layout_header,
    html.H4('Último confirmado: '+confirmado),   
    html.H4('Último disponible: '+disponible),
    #dcc.Loading(children=[html.A(['Actualizar data'],id="update-button",className="button no-print print",style={'margin': '0 auto'}),],id="update-load",style={'margin': '0 0 0 100px','float': 'left'})
])

#layout_afp = html.Div([
#    header,
#    links,
#    html.H3('Valores Fondos'),
#    dcc.Loading(id = "loading-icon_fig_vf", children=[dcc.Graph(id='fig_vf',figure = fig_vf)],type="circle"),
#    dcc.Loading(id = "loading-icon_fig_q", children=[dcc.Graph(id='fig_vf',figure = fig_q)],type="circle"),  
#])