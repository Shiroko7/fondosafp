# Using graph_objects
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from api import dif_forward_nacional

# graficos

def fig_forwards_nacional(df):
    dfc = df[df['Nombre'] == 'Compra']
    dfv = df[df['Nombre'] == 'Venta']
    dif = dif_forward_nacional(df)
    
    color=np.array(['rgb(255,255,255)']*dif['Dif'].shape[0])
    color[dif['Dif']<0]='red'
    color[dif['Dif']>=0]='green'

    hover = list()
    for i in dif['Dif']:
        if i >= 0:
            hover.append('▲ UP: ' + str(round(i,2)))
        else:
            hover.append('▼ DOWN: ' + str(round(i,2)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'],name ='Total Vendido',marker_color='RoyalBlue'))

    fig.add_trace(go.Bar(
        name = 'Dif fix',
        x = dif['Fecha'],
        y = dif['Dif'].abs(),
        marker=dict(color=color.tolist()),
        hovertext=hover
    ))

    fig.add_trace(go.Scatter(x=dfc['Fecha'],y=dfc['TOTAL'].abs(),name='Compra',marker_color='red'))
    fig.add_trace(go.Scatter(x=dfv['Fecha'],y=dfv['TOTAL'],name='Venta',marker_color='green'))

    fig.update_layout(yaxis={'title':'Total Vendido'},
                      title= 'Venta neta FWD USDCLP AFP')
    return fig

def fig_inversiones(df_input,label,tipo):
    fig = go.Figure()
    
    df = df_input[df_input['Nombre'] == label]
    if tipo == 'porcentaje':
        t = 'Porcentaje_'
        y_title = '%Fondo'
        title = label + ' Porcentaje'
    else:
        t = 'MMUSD_'
        y_title = 'MMUSD'
        title = label + ' MMUSD'
        
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'TOTAL'],name ='Total'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'A'],name ='fondo A'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'B'],name ='fondo B'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'C'],name ='fondo C'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'D'],name ='fondo D'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df[t+'E'],name ='fondo E'))

    fig.update_layout(yaxis={'title':y_title},
                      title= title)
    return fig

def fig_activos(df_input,label,tipo):
    fig = go.Figure()
    
    df = df_input[df_input['Nombre'] == label]
    if tipo == 'porcentaje':
        tipo = 'Porcentaje_'
        y_title = '%Fondo'
        title = label + ' Porcentaje'
        
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'TOTAL'],name ='Total'))
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'A'],name ='fondo A'))
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'B'],name ='fondo B'))
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'C'],name ='fondo C'))
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'D'],name ='fondo D'))
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo+'E'],name ='fondo E'))

    else:
        y_title = tipo
        title = label + ' ' + tipo
        
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[tipo],name =tipo))
        
    fig.update_layout(yaxis={'title':y_title},
                      title= 'Activos: ' + title)
    return fig


def fig_extranjeros(df):
    fig = go.Figure()
    
    columns = list(df.columns)
    columns = [i for i in columns if i != 'Nombre' and i != 'Fecha']
    for label in columns[1:]:        
        fig.add_trace(go.Scatter(x=df['Fecha'], y=df[label],name =label))

    fig.update_layout(yaxis={'title':'Extranjeros'},
                      title= 'Activos: ' + 'MMUSD')
    return fig


def fig_valor_fondos(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['VF_A'],name ='Fondo A'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['VF_B'],name ='Fondo B'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['VF_C'],name ='Fondo C'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['VF_D'],name ='Fondo D'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['VF_E'],name ='Fondo E'))

    fig.update_layout(yaxis={'title':'F Index'},
                      title= 'Fondos AFP: F Index')
    return fig

def fig_q_index(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Q_A'],name ='Fondo A'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Q_B'],name ='Fondo B'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Q_C'],name ='Fondo C'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Q_D'],name ='Fondo D'))
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Q_E'],name ='Fondo E'))

    fig.update_layout(yaxis={'title':'U Index'},
                      title= 'Fondos AFP: U Index')
    return fig



def bar_inversion_nacional(df_nacio,fondo):
    fig = go.Figure()
    fechas = df_nacio.Fecha.unique()
    y_rv = list()
    y_instr = list()
    y_bb = list()
    y_dp = list()
    y_otros = list()
    for i in fechas:
        rv = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'RENTA VARIABLE')]['Porcentaje_'+fondo]
        y_rv.append(float(rv))

        instr = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Instrumentos')]['Porcentaje_'+fondo]
       
        y_instr.append(float(instr))

        bb = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Bonos Bancarios')]['Porcentaje_'+fondo]
        y_bb.append(float(bb))

        dp = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Depósitos a Plazo')]['Porcentaje_'+fondo]
        y_dp.append(float(dp))

        rf = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'RENTA FIJA')]['Porcentaje_'+fondo]
        otros = float(rf) - float(instr) - float(bb) - float(dp)
        y_otros.append(otros)

    fig.add_trace(go.Bar(x=fechas, y=y_otros,name='RF: Otros'))
    fig.add_trace(go.Bar(x=fechas, y=y_dp,name='RF: Depósitos a Plazo'))
    fig.add_trace(go.Bar(x=fechas, y=y_bb,name='RF: Bonos Bancarios'))
    fig.add_trace(go.Bar(x=fechas, y=y_instr,name='RF: Instrumentos'))
    fig.add_trace(go.Bar(x=fechas, y=y_rv,name='Renta Variable'))



    fig.update_layout(yaxis={'title':'%Fondo'},
                      title= 'Inversión Nacional ' + fondo)
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(barmode='stack')
    return fig

def bar_inversion_internacional(df_inter,fondo):
    fig = go.Figure()
    fechas = df_inter.Fecha.unique()
    y_rv = list()
    y_rf = list()
    for i in fechas:
        rv = df_inter[(df_inter['Fecha']== i) & (df_inter['Nombre']== 'RENTA VARIABLE')]['Porcentaje_'+fondo]
        y_rv.append(float(rv))

        rf = df_inter[(df_inter['Fecha']== i) & (df_inter['Nombre']== 'RENTA FIJA')]['Porcentaje_'+fondo]
        y_rf.append(float(rf))

    fig.add_trace(go.Bar(x=fechas, y=y_rf,name='Renta Fija'))
    fig.add_trace(go.Bar(x=fechas, y=y_rv,name='Renta Variable'))

    fig.update_layout(yaxis={'title':'%Fondo'},
                      title= 'Inversión Internacional ' + fondo)
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(barmode='stack')
    return fig

def bar_inversion(df_nacio,df_inter,fondo):
    fig = go.Figure()
    fechas = df_nacio.Fecha.unique()
    y_nacio = list()
    y_inter = list()
    for i in fechas:
        nacio = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'INVERSIÓN NACIONAL TOTAL')]['Porcentaje_'+fondo]
        y_nacio.append(float(nacio))

        inter = df_inter[(df_inter['Fecha']== i) & (df_inter['Nombre']== 'INVERSIÓN EXTRANJERA')]['Porcentaje_'+fondo]
        y_inter.append(float(inter))

    fig.add_trace(go.Bar(x=fechas, y=y_nacio,name='Nacional'))
    fig.add_trace(go.Bar(x=fechas, y=y_inter,name='Internacional'))

    fig.update_layout(yaxis={'title':'%Fondo'},
                      title= 'Inversión ' + fondo)
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(barmode='stack')
    return fig


