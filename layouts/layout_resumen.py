import dash_core_components as dcc
import dash_html_components as html
import plots
import pandas as pd
from api import query_by_daterange, fetch_last_update
from datetime import date, timedelta, datetime, time

end_date = date.today() - timedelta(date.today().day)
start_date = end_date - timedelta(days=2*395)

# dataframes
df_vf = query_by_daterange("valor_fondos", start_date, end_date)
df_vf = df_vf[(df_vf != 0).all(1)]

df_q = query_by_daterange("q_index", start_date, end_date)
df_q = df_q[(df_q != 0).all(1)]

usdclp = query_by_daterange("usdclp", start_date, end_date)
usdclp = usdclp.drop_duplicates(
    subset=['Fecha'], keep='first', inplace=False, ignore_index=True).reset_index()


df_nacio = query_by_daterange(
    "inversion_nacional", start_date, end_date).dropna()
df_inter = query_by_daterange(
    "inversion_internacional", start_date, end_date).dropna()


df_fn = query_by_daterange("forwards_nacionales", start_date, end_date)
dfc = df_fn[df_fn['Nombre'] == 'Compra']
dfv = df_fn[df_fn['Nombre'] == 'Venta']


df_activos = query_by_daterange("activos", start_date, end_date).dropna()
df_bonos_clp = df_activos[df_activos['Nombre'] == 'Bonos CLP']
df_bonos_uf = df_activos[df_activos['Nombre'] == 'Bonos UF']

df_inter = query_by_daterange(
    "inversion_internacional", start_date, end_date).dropna()

df_ex = query_by_daterange(
    "inversion_internacional", start_date, end_date).dropna()
df_ex = df_ex[df_ex['Nombre'] == 'INVERSIÓN EXTRANJERA']

# plots
patrimonio_total = plots.patrimonio_ajustado(df_vf, df_q, usdclp, True)
patrimonio_afps = plots.patrimonio_ajustado(df_vf, df_q, usdclp, False)

inversiones_total = plots.bar_inversion(df_nacio, df_inter, 'TOTAL')

inter_hedge = plots.fig_hedge(df_inter, dfc, dfv, df_fn, usdclp, True)
inter_hedge_total = plots.fig_hedge_total(
    df_inter, dfc, dfv, df_fn, usdclp, True)


inversiones_nacional = plots.bar_inversion_nacional(
    df_nacio, 'TOTAL')


inversiones_internacional = plots.bar_inversion_internacional(
    df_inter, 'TOTAL')


inversiones_nacional_monedas = plots.bar_inversion_nacional_monedas(
    df_bonos_clp, df_bonos_uf, 'TOTAL')

extranjeros_total = plots.fig_total_ex_fwd(df_ex, dfc, dfv, df_fn)


extranjeros_fondos = plots.fig_inversiones(
    df_inter, 'INVERSIÓN EXTRANJERA', False)


forwards_n = plots.fig_forwards_nacional(dfc, dfv, df_fn, usdclp, True)

layout_resumen = html.Div([
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
                id='fig_patrimonio_ajustado_total', figure=patrimonio_total)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_patrimonio_ajustado_afps", children=[dcc.Graph(
                id='fig_patrimonio_ajustado_afps', figure=patrimonio_afps)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inversiones_total", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_total', figure=inversiones_total)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inter_hedge_total", children=[dcc.Graph(
                id='fig_patrimonio_inter_hedge_total', figure=inter_hedge_total)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inter_hedge", children=[dcc.Graph(
                id='fig_patrimonio_inter_hedge', figure=inter_hedge)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_inversiones_nacional", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_nacional', figure=inversiones_nacional)], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Loading(id="loading_inversiones_nacional_monedas", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_nacional_monedas', figure=inversiones_nacional_monedas)], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            dcc.Loading(id="loading_inversiones_internacional", children=[dcc.Graph(
                id='fig_patrimonio_inversiones_internacional', figure=inversiones_internacional)], type="circle"),
        ], className='pretty_container'
    ),
    html.H4('Inversión Internacional'),
    html.Div(
        [
            dcc.Loading(id="loading_extranjeros_total", children=[dcc.Graph(
                id='fig_patrimonio_extranjeros_total', figure=extranjeros_total)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_extranjeros_fondos", children=[dcc.Graph(
                id='fig_patrimonio_extranjeros_fondos', figure=extranjeros_fondos)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading_forwards_n", children=[dcc.Graph(
                id='fig_patrimonio_forwards_n', figure=forwards_n)], type="circle"),
        ], className='pretty_container'
    ),
])
