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


#dataframes

df_fn = query_by_daterange("forwards_nacionales",start_date,end_date).dropna()
df_inter = query_by_daterange("inversion_internacional",start_date,end_date).dropna()
df_nacio = query_by_daterange("inversion_nacional",start_date,end_date).dropna()
df_total = query_by_daterange("inversion_total",start_date,end_date).dropna()
df_activos = query_by_daterange("activos",start_date,end_date).dropna()
df_extranjeros = query_by_daterange("extranjeros",start_date,end_date).dropna()
df_vf = query_by_daterange("valor_fondos",start_date,end_date).dropna()
df_q = query_by_daterange("q_index",start_date,end_date).dropna()




#layout forwards nacionales
figure_fn = plots.fig_forwards_nacional(df_fn,df_vf,df_q)

bar_nacio = plots.bar_inversion_nacional(df_nacio,'TOTAL')
bar_inter = plots.bar_inversion_internacional(df_inter,'TOTAL')
bar_inver = plots.bar_inversion(df_nacio,df_inter,'TOTAL')

fig_inv_total = plots.fig_inversiones(df_total,'TOTAL ACTIVOS','MMUSD')

fig_inter_hedge = plots.fig_hedge(df_inter,df_fn)


#layout inversiones afp nacionales
fig_inv_na = plots.fig_inversiones(df_nacio,'INVERSIÓN NACIONAL TOTAL','MMUSD')
fig_inv_na_rv = plots.fig_inversiones(df_nacio,'RENTA VARIABLE','MMUSD')
fig_inv_na_rf = plots.fig_inversiones(df_nacio,'RENTA FIJA','MMUSD')
fig_inv_na_ins = plots.fig_inversiones(df_nacio,'Instrumentos','MMUSD')
fig_inv_na_bb = plots.fig_inversiones(df_nacio,'Bonos Bancarios','MMUSD')
fig_inv_na_dp = plots.fig_inversiones(df_nacio,'Depósitos a Plazo','MMUSD')

#layout inversiones afp extranjeras
fig_inv_ex = plots.fig_inversiones(df_inter,'INVERSIÓN EXTRANJERA','MMUSD')
fig_inv_ex_rv = plots.fig_inversiones(df_inter,'RENTA FIJA','MMUSD')
fig_inv_ex_rf = plots.fig_inversiones(df_inter,'RENTA VARIABLE','MMUSD')


#layout activos de pensiones
fig_act_bclp = plots.fig_activos(df_activos,'Bonos CLP','porcentaje')
fig_act_buf = plots.fig_activos(df_activos,'Bonos UF','porcentaje')
fig_act_ex = plots.fig_activos(df_activos,'TOTAL EXTRANJERO','porcentaje')

fig_ex_reg = plots.fig_extranjeros(df_extranjeros)

#layout vfs
#fig_vf = plots.fig_valor_fondos(df_vf)
#fig_q = plots.fig_q_index(df_q)

header = html.Div(
            [
                html.Div(
                    [
                        html.H2('AFP Data',),
                        html.H6('Versión Beta 1.8.1',className='no-print'),
                    ],className='nine columns',style = {'text-align': 'center', 'margin-right': '16.6%'}
                )
            ],className='nine columns',
        )


links = html.Div(
    [
        html.Ul(
            [
                html.Li([dcc.Link('Datos Principales', href='/apps/datos-principales'),]),
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
    html.A(['Actualizar data'],id="update-button",className="button no-print print",style={'margin': '0 auto'}),
])


layout_datos = html.Div([
    layout_header,
    html.H3('Forwards Nacionales'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fn", children=[dcc.Graph(id='fig_fn',figure = figure_fn)],type="circle"),
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
    
])

layout_nacional = html.Div([
    layout_header,

    html.H3('Inversión Nacional'),
    html.Div(
        [
            dcc.Checklist(id='check_fig-na', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na", children=[dcc.Graph(id='fig-na',figure = fig_inv_na)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rv', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_rv", children=[dcc.Graph(id='fig-na_rv',figure = fig_inv_na_rv)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_rf', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_rf", children=[dcc.Graph(id='fig-na_rf',figure = fig_inv_na_rf)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_ins', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_ins", children=[dcc.Graph(id='fig-na_ins',figure = fig_inv_na_ins)],type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Checklist(id='check_fig-na_bb', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_bb", children=[dcc.Graph(id='fig-na_bb',figure = fig_inv_na_bb)],type="circle"),
        ], className='pretty_container'
    ),
    
    html.Div(
        [
            dcc.Checklist(id='check_fig-na_dp', options=[{'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id = "loading-icon_fig-na_dp", children=[dcc.Graph(id='fig-na_dp',figure = fig_inv_na_dp)],type="circle"),
        ], className='pretty_container'
    ),

])

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


layout_extranjeros = html.Div([
    layout_header,
    html.H3('Inversión en Regiones'),
    html.Div(
        [
            dcc.Loading(id = "loading-icon_fig-ex_reg", children=[dcc.Graph(id='fig-ex_reg',figure = fig_ex_reg)],type="circle"),  
        ], className='pretty_container'
    ),

])


#layout_afp = html.Div([
#    header,
#    links,
#    html.H3('Valores Fondos'),
#    dcc.Loading(id = "loading-icon_fig_vf", children=[dcc.Graph(id='fig_vf',figure = fig_vf)],type="circle"),
#    dcc.Loading(id = "loading-icon_fig_q", children=[dcc.Graph(id='fig_vf',figure = fig_q)],type="circle"),  
#])