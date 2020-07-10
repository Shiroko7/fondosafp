# Using graph_objects
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from api import dif_forward_nacional

# graficos

def fig_forwards_nacional(df,usdclp, df_vf, df_q):
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
    #forwards 
    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'], yaxis="y", name ='Pos Neta Fwd (Vendida)', marker_color='RoyalBlue'))

    fig.add_trace(go.Bar(
        name = 'Cambio en Pos Neta Fwd',
        x = dif['Fecha'],
        y = dif['Dif'].abs(),
        marker=dict(color=color.tolist()),
        hovertext=hover
    ))

    fig.add_trace(go.Scatter(x=dfc['Fecha'],y=dfc['TOTAL'].abs(), yaxis="y", name='Pos Comprada Fwd', marker_color='red',visible="legendonly"))
    fig.add_trace(go.Scatter(x=dfv['Fecha'],y=dfv['TOTAL'], yaxis="y", name='Pos Vendida Fwd', marker_color='green',visible="legendonly"))
    fig.add_trace(go.Scatter(x=usdclp['Fecha'],y=usdclp['Precio'], yaxis="y2", name='USD/CLP', marker_color='orange', visible="legendonly"))
    
    # Create axis objects
    fig.update_layout(
        xaxis=dict(
            domain=[0.1, 1]
        ),
        yaxis=dict(
            title="Forwards",
            titlefont=dict(
                color="RoyalBlue"
            ),
            tickfont=dict(
                color="RoyalBlue"
            ),
            position=0
        ),
        yaxis2=dict(
            title="CLP",
            titlefont=dict(
                color="orange"
            ),
            tickfont=dict(
                color="orange"
            ),
            anchor="x",
            overlaying="y",
            position=0.1
        ),
    )

    fig.update_layout(title= 'Venta neta FWD USDCLP')
    
    return fig

def clp_to_usd(df,usdclp):
    #print(usdclp.columns)
    #usdclp['Fecha'] = usdclp['Fecha'].str.slice(stop=10)
    usdclp['Fecha'] = pd.to_datetime(usdclp['Fecha'])
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    for i in range(len(df)): 
        fx = usdclp[usdclp['Fecha'] == df.loc[i,'Fecha']]['Precio']    

        if fx is not None and len(fx) > 0:
            #print(df.loc[i,'VF_A'] )
            #print(fx.squeeze())
            df.loc[i,'VF_A'] = df.loc[i,'VF_A'] / fx.squeeze()
            df.loc[i,'VF_B'] = df.loc[i,'VF_B'] / fx.squeeze()
            df.loc[i,'VF_C'] = df.loc[i,'VF_C'] / fx.squeeze()
            df.loc[i,'VF_D'] = df.loc[i,'VF_D'] / fx.squeeze()
            df.loc[i,'VF_E'] = df.loc[i,'VF_E'] / fx.squeeze()
        else:
            df.loc[i,'VF_A'] = df.loc[i,'VF_A'] / 820
            df.loc[i,'VF_B'] = df.loc[i,'VF_B'] / 820
            df.loc[i,'VF_C'] = df.loc[i,'VF_C'] / 820
            df.loc[i,'VF_D'] = df.loc[i,'VF_D'] / 820
            df.loc[i,'VF_E'] = df.loc[i,'VF_E'] / 820
    
    return df


def fig_afp(df_vf, usdclp):
    
    df_vf = clp_to_usd(df_vf,usdclp)

    fig = go.Figure()

    #fondos
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_A'], name ='Patrimonio Fondo A'))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_B'], name ='Patrimonio Fondo B',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_C'], name ='Patrimonio Fondo C'))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_D'], name ='Patrimonio Fondo D',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_E'], name ='Patrimonio Fondo E'))


    #fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_A'], yaxis="y3", name ='Cambios de Fondo A',visible="legendonly"))
    #fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_B'], yaxis="y3", name ='Cambios de Fondo B',visible="legendonly"))
    #fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_C'], yaxis="y3", name ='Cambios de Fondo C',visible="legendonly"))
    #fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_D'], yaxis="y3", name ='Cambios de Fondo D',visible="legendonly"))
    #fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_E'], yaxis="y3", name ='Cambios de Fondo E',visible="legendonly"))

    fig.update_layout(yaxis={'title':"USD"},
                      title= "Patrimonio Fondos de Pensiones")
    
    return fig

def fig_forwards_nacional_afp(df, usdclp,df_vf, df_q):
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
    #forwards 
    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'], yaxis="y", name ='Pos Neta Fwd (Vendida)', marker_color='RoyalBlue'))

    fig.add_trace(go.Bar(
        name = 'Cambio en Pos Neta Fwd',
        x = dif['Fecha'],
        y = dif['Dif'].abs(),
        marker=dict(color=color.tolist()),
        hovertext=hover
    ))

    fig.add_trace(go.Scatter(x=dfc['Fecha'],y=dfc['TOTAL'].abs(), yaxis="y", name='Pos Comprada Fwd', marker_color='red',visible="legendonly"))
    fig.add_trace(go.Scatter(x=dfv['Fecha'],y=dfv['TOTAL'], yaxis="y", name='Pos Vendida Fwd', marker_color='green',visible="legendonly"))
    fig.add_trace(go.Scatter(x=usdclp['Fecha'],y=usdclp['Precio'], yaxis="y4", name='USD/CLP', marker_color='orange',visible="legendonly"))

    #fondos
    df_vf = clp_to_usd(df_vf,usdclp)

    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_A'],yaxis="y2", name ='Patrimonio Fondo A',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_B'],yaxis="y2", name ='Patrimonio Fondo B',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_C'],yaxis="y2", name ='Patrimonio Fondo C',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_D'],yaxis="y2", name ='Patrimonio Fondo D',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_vf['Fecha'], y=df_vf['VF_E'],yaxis="y2", name ='Patrimonio Fondo E',visible="legendonly"))


    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_A'], yaxis="y3", name ='Cambios de Fondo A',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_B'], yaxis="y3", name ='Cambios de Fondo B',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_C'], yaxis="y3", name ='Cambios de Fondo C',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_D'], yaxis="y3", name ='Cambios de Fondo D',visible="legendonly"))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_E'], yaxis="y3", name ='Cambios de Fondo E',visible="legendonly"))

    # Create axis objects
    fig.update_layout(
        xaxis=dict(
            domain=[0.1, 0.8]
        ),
        yaxis=dict(
            title="Forwards",
            titlefont=dict(
                color="RoyalBlue"
            ),
            tickfont=dict(
                color="RoyalBlue"
            ),
            position=0
        ),
        yaxis2=dict(
            title="AFP Fondos USD",
            titlefont=dict(
                color="#101414"
            ),
            tickfont=dict(
                color="#101414"
            ),
            anchor="x",
            overlaying="y",
            side="right",
            position=0.8
        ),
        yaxis3=dict(
            title="AFP Index de Cambio",
            titlefont=dict(
                color="#323838"
            ),
            tickfont=dict(
                color="#323838"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=0.9
        ),
        yaxis4=dict(
            title="USDCLP",
            titlefont=dict(
                color="orange"
            ),
            tickfont=dict(
                color="orange"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.1
        )
    )

    fig.update_layout(title= 'Venta neta FWD USDCLP AFP')
    
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
    if label == 'Instrumentos':
        title = 'Inversión en Bonos de Tesorería y Centrales'    
    
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


def fig_hedge(df_inter,df_fn):
    df_fn = dif_forward_nacional(df_fn)
    fig = go.Figure()
    df_inter = df_inter[df_inter['Nombre'] == 'INVERSIÓN EXTRANJERA'].reset_index()
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['TOTAL']/df_inter['MMUSD_TOTAL']*100,name ='Total'))
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['Fondo_A']/df_inter['MMUSD_A']*100,name ='fondo A'))
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['Fondo_B']/df_inter['MMUSD_B']*100,name ='fondo B'))
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['Fondo_C']/df_inter['MMUSD_C']*100,name ='fondo C'))
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['Fondo_D']/df_inter['MMUSD_D']*100,name ='fondo D'))
    fig.add_trace(go.Scatter(x=df_inter['Fecha'], y=df_fn['Fondo_E']/df_inter['MMUSD_E']*100,name ='fondo E'))    

    fig.update_layout(yaxis={'title':'%Fondo'},
                      title= 'Porcentaje Inversión Extranjera Hedge')

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

        y_rv.append(float(rv.squeeze()))

        instr = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Instrumentos')]['Porcentaje_'+fondo]
       
        y_instr.append(float(instr.squeeze()))

        bb = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Bonos Bancarios')]['Porcentaje_'+fondo]
        y_bb.append(float(bb.squeeze()))

        dp = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'Depósitos a Plazo')]['Porcentaje_'+fondo]
        y_dp.append(float(dp.squeeze()))

        rf = df_nacio[(df_nacio['Fecha']== i) & (df_nacio['Nombre']== 'RENTA FIJA')]['Porcentaje_'+fondo]
        otros = float(rf.squeeze()) - float(instr.squeeze()) - float(bb.squeeze()) - float(dp.squeeze())
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


