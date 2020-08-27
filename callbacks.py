from dash.dependencies import Input, Output, State
import plots
import dash_html_components as html
import pandas as pd
from app import app
from api import query_by_daterange


# LAYOUT FORWARDS
@app.callback([Output('fig_fn', 'figure'),
               Output('fig_inter_hedge_total', 'figure'),
               Output('fig_inter_hedge', 'figure'),
               Output('fig_afp', 'figure'),
               Output('fig_fn_afp', 'figure')],
              [Input(component_id='daterange_forwards', component_property='start_date'),
               Input(component_id='daterange_forwards', component_property='end_date'), ])
def update_fig_fn(start_date, end_date):
    # DATAFRAMES

    df_fn = query_by_daterange("forwards_nacionales", start_date, end_date)

    dfc = df_fn[df_fn['Nombre'] == 'Compra']

    dfv = df_fn[df_fn['Nombre'] == 'Venta']

    df_vf = query_by_daterange("valor_fondos", start_date, end_date)
    df_vf = df_vf[(df_vf != 0).all(1)]

    df_q = query_by_daterange("q_index", start_date, end_date)
    df_q = df_q[(df_q != 0).all(1)]

    usdclp = query_by_daterange("usdclp", start_date, end_date)
    usdclp = usdclp.drop_duplicates(
        subset=['Fecha'], keep='first', inplace=False, ignore_index=True).reset_index()

    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date)

    # FIGURES
    fig_fn = plots.fig_forwards_nacional(dfc, dfv, df_fn, usdclp)

    fig_inter_hedge = plots.fig_hedge(df_inter, dfc, dfv, df_fn, usdclp)
    fig_inter_hedge_total = plots.fig_hedge_total(
        df_inter, dfc, dfv, df_fn, usdclp)

    fig_afp = plots.fig_afp(df_vf, usdclp)

    fig_fn_afp = plots.fig_forwards_nacional_afp(
        dfc, dfv, df_fn, usdclp, df_vf, df_q)

    return fig_fn, fig_inter_hedge_total, fig_inter_hedge, fig_afp, fig_fn_afp

# LAYOUT INVERSIONES


@app.callback(
    Output('fig_inv_total', 'figure'),
    [
        Input(component_id='daterange_inversiones',
              component_property='start_date'),
        Input(component_id='daterange_inversiones', component_property='end_date'), ],
)
def update_fig_inver(start_date, end_date):
    df_total = query_by_daterange(
        "inversion_total", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_total, 'TOTAL ACTIVOS', 'MMUSD')

    return fig


@app.callback(
    Output('fig_bar_inver', 'figure'),
    [Input('dropdown_bar-inver', 'value'),
     Input(component_id='daterange_inversiones',
           component_property='start_date'),
     Input(component_id='daterange_inversiones', component_property='end_date'), ],
)
def update_bar_inver(value, start_date, end_date):
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()

    fig = plots.bar_inversion(df_nacio, df_inter, value)

    return fig


@app.callback(
    Output('fig_bar_nacio_monedas', 'figure'),
    [Input('dropdown_bar-nacio_monedas', 'value'),
     Input(component_id='daterange_inversiones',
           component_property='start_date'),
     Input(component_id='daterange_inversiones', component_property='end_date'), ],
)
def update_bar_nacio_monedas(value, start_date, end_date):
    df = query_by_daterange("activos", start_date, end_date).dropna()
    df_bonos_clp = df[df['Nombre'] == 'Bonos CLP']
    df_bonos_uf = df[df['Nombre'] == 'Bonos UF']
    fig = plots.bar_inversion_nacional_monedas(
        df_bonos_clp, df_bonos_uf, value)

    return fig


@app.callback(
    Output('fig_bar_nacio', 'figure'),
    [Input('dropdown_bar-nacio', 'value'),
     Input(component_id='daterange_inversiones',
           component_property='start_date'),
     Input(component_id='daterange_inversiones', component_property='end_date'), ],
)
def update_bar_nacio(value, start_date, end_date):
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.bar_inversion_nacional(df_nacio, value)

    return fig


@app.callback(
    Output('fig_bar_inter', 'figure'),
    [Input('dropdown_bar-inter', 'value'),
     Input(component_id='daterange_inversiones',
           component_property='start_date'),
     Input(component_id='daterange_inversiones', component_property='end_date'), ],
)
def update_bar_inter(value, start_date, end_date):
    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()
    fig = plots.bar_inversion_internacional(df_inter, value)

    return fig

# LAYOUT NACIONAL


@app.callback(
    Output('fig_na', 'figure'),
    [Input('check_fig-na', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'INVERSIÓN NACIONAL TOTAL', flag)
    return fig


@app.callback(
    Output('fig_na_rv', 'figure'),
    [Input('check_fig-na_rv', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output_rv(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'RENTA VARIABLE', flag)
    return fig


@app.callback(
    Output('fig_na_rf', 'figure'),
    [Input('check_fig-na_rf', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output_rf(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'RENTA FIJA', flag)
    return fig


@app.callback(
    Output('fig_na_ins', 'figure'),
    [Input('check_fig-na_ins', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output_ins(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'Instrumentos', flag)
    return fig


@app.callback(
    Output('fig_na_bb', 'figure'),
    [Input('check_fig-na_bb', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output_bb(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'Bonos Bancarios', flag)
    return fig


@app.callback(
    Output('fig_na_dp', 'figure'),
    [Input('check_fig-na_dp', 'value'),
     Input(component_id='daterange_nacional', component_property='start_date'),
     Input(component_id='daterange_nacional', component_property='end_date')]
)
def update_output_dp(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    # dataset
    df_nacio = query_by_daterange(
        "inversion_nacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_nacio, 'Depósitos a Plazo', flag)
    return fig

# LAYOUT INTERNACIONAL


@app.callback(
    Output('fig_ex-fwd', 'figure'),
    [Input(component_id='daterange_internacional', component_property='start_date'),
     Input(component_id='daterange_internacional', component_property='end_date')]
)
def update_output_ex_fwd(start_date, end_date):
    df_ex = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()
    df_ex = df_ex[df_ex['Nombre'] == 'INVERSIÓN EXTRANJERA']

    df_fn = query_by_daterange("forwards_nacionales", start_date, end_date)

    dfc = df_fn[df_fn['Nombre'] == 'Compra']

    dfv = df_fn[df_fn['Nombre'] == 'Venta']

    fig = plots.fig_total_ex_fwd(df_ex, dfc, dfv, df_fn)
    return fig


@app.callback(
    Output('fig_ex', 'figure'),
    [Input('check_fig-ex', 'value'),
     Input(component_id='daterange_internacional',
           component_property='start_date'),
     Input(component_id='daterange_internacional', component_property='end_date')]
)
def update_output_ex(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_inter, 'INVERSIÓN EXTRANJERA', flag)
    return fig


@app.callback(
    Output('fig_ex_rv', 'figure'),
    [Input('check_fig-ex_rv', 'value'),
     Input(component_id='daterange_internacional',
           component_property='start_date'),
     Input(component_id='daterange_internacional', component_property='end_date')]
)
def update_output_ex_rv(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_inter, 'RENTA VARIABLE', flag)
    return fig


@app.callback(
    Output('fig_ex_rf', 'figure'),
    [Input('check_fig-ex_rf', 'value'),
     Input(component_id='daterange_internacional',
           component_property='start_date'),
     Input(component_id='daterange_internacional', component_property='end_date')]
)
def update_output_ex_rf(value, start_date, end_date):
    flag = "MMUSD"
    if value is not None:
        if len(value) != 0:
            flag = "porcentaje"
    df_inter = query_by_daterange(
        "inversion_internacional", start_date, end_date).dropna()
    fig = plots.fig_inversiones(df_inter, 'RENTA FIJA', flag)
    return fig


# LAYOUT ACTIVOS
@app.callback(
    [Output('fig_act_bclp', 'figure'),
     Output('fig_act_buf', 'figure'),
     Output('fig_act_ex', 'figure'),
     ],
    [
        Input(component_id='daterange_activos',
              component_property='start_date'),
        Input(component_id='daterange_activos', component_property='end_date')]
)
def update_activos(start_date, end_date):
    # dataset
    df_activos = query_by_daterange("activos", start_date, end_date).dropna()

    # layout activos de pensiones
    fig_act_bclp = plots.fig_activos(df_activos, 'Bonos CLP', 'porcentaje')
    fig_act_buf = plots.fig_activos(df_activos, 'Bonos UF', 'porcentaje')
    fig_act_ex = plots.fig_activos(
        df_activos, 'TOTAL EXTRANJERO', 'porcentaje')
    return fig_act_bclp, fig_act_buf, fig_act_ex

# LAYOUT EXTRANJEROS


@app.callback(
    Output('fig_ex_reg', 'figure'),
    [
        Input(component_id='daterange_extranjeros',
              component_property='start_date'),
        Input(component_id='daterange_extranjeros', component_property='end_date')]
)
def update_activos(start_date, end_date):
    df_extranjeros = query_by_daterange(
        "extranjeros", start_date, end_date).dropna()
    fig_ex_reg = plots.fig_extranjeros(df_extranjeros)
    return fig_ex_reg


##########################
@app.callback(
    Output('update-load', 'children'),
    [Input('update-button', 'n_clicks')]
)
def update_button(n_clicks):
    if n_clicks is not None:
        auto_update()
        return html.Div("Actualizado")
    return [html.A(['Actualizar data'], id="update-button", className="button no-print print", style={'margin': '0 auto'})]
