import dash_core_components as dcc
import dash_html_components as html
import plots
from api import query_by_daterange
from datetime import date, timedelta, datetime, time

start_date = date(2016,1,1)
end_date = date(2020,5,1)

df_fn = query_by_daterange("forwards_nacionales",start_date,end_date)
df_inter = query_by_daterange("inversion_internacional",start_date,end_date)
df_nacio = query_by_daterange("inversion_nacional",start_date,end_date)
df_total = query_by_daterange("inversion_total",start_date,end_date)
df_activos = query_by_daterange("activos",start_date,end_date)
df_extranjeros = query_by_daterange("extranjeros",start_date,end_date)
df_vf = query_by_daterange("valor_fondos",start_date,end_date)
df_q = query_by_daterange("q_index",start_date,end_date)

#layout forwards nacionales
figure_fn = plots.fig_forwards_nacional(df_fn)

#layout inversiones afp
bar_nacio = plots.bar_inversion_nacional(df_nacio,'TOTAL')
bar_inter = plots.bar_inversion_internacional(df_inter,'TOTAL')
bar_inver = plots.bar_inversion(df_nacio,df_inter,'TOTAL')

fig_inv_ex = plots.fig_inversiones(df_inter,'INVERSIÓN EXTRANJERA','porcentaje')
fig_inv_ex_rv = plots.fig_inversiones(df_inter,'RENTA FIJA','porcentaje')
fig_inv_ex_rf = plots.fig_inversiones(df_inter,'RENTA VARIABLE','porcentaje')

fig_inv_na = plots.fig_inversiones(df_nacio,'INVERSIÓN NACIONAL TOTAL','porcentaje')
fig_inv_na_rv = plots.fig_inversiones(df_nacio,'RENTA VARIABLE','porcentaje')
fig_inv_na_rf = plots.fig_inversiones(df_nacio,'RENTA FIJA','porcentaje')
fig_inv_na_ins = plots.fig_inversiones(df_nacio,'Instrumentos','porcentaje')
fig_inv_na_bb = plots.fig_inversiones(df_nacio,'Bonos Bancarios','porcentaje')
fig_inv_na_dp = plots.fig_inversiones(df_nacio,'Depósitos a Plazo','porcentaje')

fig_inv_total = plots.fig_inversiones(df_total,'TOTAL ACTIVOS','MMUSD')

#layout activos de pensiones
fig_act_bclp = plots.fig_activos(df_activos,'Bonos CLP','porcentaje')
fig_act_buf = plots.fig_activos(df_activos,'Bonos UF','porcentaje')
fig_act_ex = plots.fig_activos(df_activos,'TOTAL EXTRANJERO','porcentaje')

fig_ex_reg = plots.fig_extranjeros(df_extranjeros)

#layout vfs
fig_vf = plots.fig_valor_fondos(df_vf)
fig_q = plots.fig_q_index(df_q)

header = html.Div(
            [
                html.Div(
                    [
                        html.H2('AFP Data',),
                        html.H6('Versión Beta 1.0.1',className='no-print'),
                    ],className='twelve columns',style = {'text-align': 'center'}
                )
            ],id='header',className='row',
        )


layout_fn = html.Div([
    header,
    html.Ul(
        [
            html.Li([dcc.Link('Inversiones', href='/apps/inversiones'),]),
            html.Li([dcc.Link('Activos de Pensiones', href='/apps/activos'),]),
            html.Li([dcc.Link('Valores Fondos', href='/apps/valores'),]),
            html.Li([dcc.Link('Inversión en Regiones', href='/apps/extranjeros'),]),
        ]
    ),  
    html.H3('Forwards Nacionales'),
    dcc.Loading(id = "loading-icon_fn", children=[dcc.Graph(id='fig_fn',figure = figure_fn)],type="circle"),
])

layout_inversiones = html.Div([
    header,
    html.Ul(
        [
            html.Li([dcc.Link('Forwards Nacionales', href='/apps/forwards-nacionales'),]),
            html.Li([dcc.Link('Activos de Pensiones', href='/apps/activos'),]),
            html.Li([dcc.Link('Valores Fondos', href='/apps/valores'),]),
            html.Li([dcc.Link('Inversión en Regiones', href='/apps/extranjeros'),]),
        ]
    ),  
    html.H3('Inversiones'),    
    html.H5('Gráficos de Barra'),
    dcc.Loading(id = "loading-icon_bar-inver", children=[dcc.Graph(id='fig_bar-inver',figure = bar_inver)],type="circle"),    
    dcc.Loading(id = "loading-icon_bar-nacio", children=[dcc.Graph(id='fig_bar-nacio',figure = bar_nacio)],type="circle"),
    dcc.Loading(id = "loading-icon_bar-inter", children=[dcc.Graph(id='fig_bar-inter',figure = bar_inter)],type="circle"),    

    html.H5('Series de tiempo'),
    html.H6('Inversión Nacional'),
    dcc.Loading(id = "loading-icon_fig-na", children=[dcc.Graph(id='fig-na',figure = fig_inv_na)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-na_rv", children=[dcc.Graph(id='fig-na_rv',figure = fig_inv_na_rv)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-na_rf", children=[dcc.Graph(id='fig-na_rf',figure = fig_inv_na_rf)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-na_ins", children=[dcc.Graph(id='fig-na_ins',figure = fig_inv_na_ins)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-na_bb", children=[dcc.Graph(id='fig-na_bb',figure = fig_inv_na_bb)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-na_dp", children=[dcc.Graph(id='fig-na_dp',figure = fig_inv_na_dp)],type="circle"),

    html.H6('Inversión Internacional'),
    dcc.Loading(id = "loading-icon_fig-ex", children=[dcc.Graph(id='fig-ex',figure = fig_inv_ex)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-ex_rv", children=[dcc.Graph(id='fig-ex_rv',figure = fig_inv_ex_rv)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-ex_rf", children=[dcc.Graph(id='fig-ex_rf',figure = fig_inv_ex_rf)],type="circle"),

    html.H6('Inversión Total'),
    dcc.Loading(id = "loading-icon_fig-inv_total", children=[dcc.Graph(id='fig-inv_total',figure = fig_inv_total)],type="circle"),
])

layout_activos = html.Div([
    header,
    html.Ul(
        [
            html.Li([dcc.Link('Forwards Nacionales', href='/apps/forwards-nacionales'),]),
            html.Li([dcc.Link('Inversiones', href='/apps/inversiones'),]),
            html.Li([dcc.Link('Valores Fondos', href='/apps/valores'),]),
            html.Li([dcc.Link('Inversión en Regiones', href='/apps/extranjeros'),]),
        ]
    ), 

    html.H3('Activos de Pensiones'),
    dcc.Loading(id = "loading-icon_fig-act_bclp", children=[dcc.Graph(id='fig-act_bclp',figure = fig_act_bclp)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-act_buf", children=[dcc.Graph(id='fig-act_buf',figure = fig_act_buf)],type="circle"),
    dcc.Loading(id = "loading-icon_fig-act_ex", children=[dcc.Graph(id='fig-act_ex',figure = fig_act_ex)],type="circle"),
])


layout_extranjeros = html.Div([
    header,
    html.Ul(
        [
            html.Li([dcc.Link('Forwards Nacionales', href='/apps/forwards-nacionales'),]),
            html.Li([dcc.Link('Inversiones', href='/apps/inversiones'),]),
            html.Li([dcc.Link('Valores Fondos', href='/apps/valores'),]),
            html.Li([dcc.Link('Activos de Pensiones', href='/apps/activos'),]),
        ]
    ),  

    html.H3('Inversión en Regiones'),
    dcc.Loading(id = "loading-icon_fig-ex_reg", children=[dcc.Graph(id='fig-ex_reg',figure = fig_ex_reg)],type="circle"),  
])


layout_afp = html.Div([
    header,
    html.Ul(
        [
            html.Li([dcc.Link('Forwards Nacionales', href='/apps/forwards-nacionales'),]),
            html.Li([dcc.Link('Inversiones', href='/apps/inversiones'),]),
            html.Li([dcc.Link('Activos de Pensiones', href='/apps/activos'),]),
            html.Li([dcc.Link('Inversión en Regiones', href='/apps/extranjeros'),]),
        ]
    ),  
    html.H3('Valores Fondos'),
    dcc.Loading(id = "loading-icon_fig_vf", children=[dcc.Graph(id='fig_vf',figure = fig_vf)],type="circle"),
    dcc.Loading(id = "loading-icon_fig_q", children=[dcc.Graph(id='fig_vf',figure = fig_q)],type="circle"),  
])