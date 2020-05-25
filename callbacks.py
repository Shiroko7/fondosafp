from dash.dependencies import Input, Output
import plots
from app import app
from layouts import df_nacio, df_inter

@app.callback(
    Output('fig-na', 'figure'),
    [Input('check_fig-na', 'value'),]
)
def update_output(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'INVERSIÓN NACIONAL TOTAL',flag)
    return fig
    
@app.callback(
    Output('fig-na_rv', 'figure'),
    [Input('check_fig-na_rv', 'value'),]
)
def update_output_rv(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'RENTA VARIABLE',flag)
    return fig
    
@app.callback(
    Output('fig-na_rf', 'figure'),
    [Input('check_fig-na_rf', 'value'),]
)
def update_output_rf(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'RENTA FIJA',flag)
    return fig

@app.callback(
    Output('fig-na_ins', 'figure'),
    [Input('check_fig-na_ins', 'value'),]
)
def update_output_ins(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'Instrumentos',flag)
    return fig

@app.callback(
    Output('fig-na_bb', 'figure'),
    [Input('check_fig-na_bb', 'value'),]
)
def update_output_bb(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'Bonos Bancarios',flag)
    return fig

@app.callback(
    Output('fig-na_dp', 'figure'),
    [Input('check_fig-na_dp', 'value'),]
)
def update_output_dp(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_nacio,'Depósitos a Plazo',flag)
    return fig
    
@app.callback(
    Output('fig-ex', 'figure'),
    [Input('check_fig-ex', 'value'),]
)
def update_output_ex(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_inter,'INVERSIÓN EXTRANJERA',flag)
    return fig

@app.callback(
    Output('fig-ex_rv', 'figure'),
    [Input('check_fig-ex_rv', 'value'),]
)
def update_output_ex_rv(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_inter,'RENTA VARIABLE',flag)
    return fig

@app.callback(
    Output('fig-ex_rf', 'figure'),
    [Input('check_fig-ex_rf', 'value'),]
)
def update_output_ex_rf(value):
    flag = "MMUSD"
    if value is not None:
        if len(value)!=0:
            flag = "porcentaje"

    fig = plots.fig_inversiones(df_inter,'RENTA FIJA',flag)
    return fig
    
@app.callback(
    Output('fig_bar-inver', 'figure'),
    [Input('dropdown_bar-inver', 'value'),]
)
def update_bar_inver(value):

    fig = plots.bar_inversion(df_nacio,df_inter,value)

    return fig

@app.callback(
    Output('fig_bar-nacio', 'figure'),
    [Input('dropdown_bar-nacio', 'value'),]
)
def update_bar_nacio(value):

    fig = plots.bar_inversion_nacional(df_nacio,value)

    return fig

@app.callback(
    Output('fig_bar-inter', 'figure'),
    [Input('dropdown_bar-inter', 'value'),]
)
def update_bar_inter(value):

    fig = plots.bar_inversion_internacional(df_inter,value)

    return fig