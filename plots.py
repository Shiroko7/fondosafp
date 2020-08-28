# Using graph_objects
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from api import dif_forward_nacional

# graficos


def fig_forwards_nacional(dfc, dfv, df, usdclp, resumen=False):
    dif = dif_forward_nacional(dfc, dfv, df)

    color = np.array(['rgb(255,255,255)']*dif['Dif'].shape[0])
    color[dif['Dif'] < 0] = 'red'
    color[dif['Dif'] >= 0] = 'green'

    hover = list()
    for i in dif['Dif']:
        if i >= 0:
            hover.append('▲ UP: ' + str(round(i, 2)))
        else:
            hover.append('▼ DOWN: ' + str(round(i, 2)))

    fig = go.Figure()
    # forwards
    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'], yaxis="y",
                             name='Pos Neta Fwd (Vendida)', marker_color='RoyalBlue', hovertemplate='%{x}, %{y:.1f}'))
    # hovertemplate='$%{y:,.0f}' + '<br>%{x}</br>'))

    if resumen:
        fig.add_trace(go.Scatter(x=dfc['Fecha'], y=dfc['TOTAL'].abs(
        ), yaxis="y", name='Pos Comprada Fwd', marker_color='red', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=dfv['Fecha'], y=dfv['TOTAL'], yaxis="y",
                                 name='Pos Vendida Fwd', marker_color='green', hovertemplate='%{x}, %{y:.1f}'))
    else:
        fig.add_trace(go.Scatter(x=dfv['Fecha'], y=dfv['TOTAL'], yaxis="y",
                                 name='Pos Vendida Fwd', marker_color='green', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=usdclp['Fecha'], y=usdclp['Precio'], yaxis="y2",
                                 name='USD/CLP', marker_color='orange', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))

    fig.add_trace(go.Bar(
        name='Cambio en Pos Neta Fwd',
        x=dif['Fecha'],
        y=dif['Dif'].abs(),
        marker=dict(color=color.tolist()),
        hovertext=hover
    ))

    # Create axis objects
    if not resumen:
        fig.update_layout(
            xaxis=dict(
                domain=[0.1, 1]
            ),
            yaxis=dict(
                title="Forwards MMUSD",
                titlefont=dict(
                    color="RoyalBlue"
                ),
                tickfont=dict(
                    color="RoyalBlue"
                ),
                position=0,
                dtick=5000
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
    else:
        fig.update_layout(
            yaxis=dict(
                title="MMUSD",
                dtick=5000
            ),
        )
        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[0, max(dfv['TOTAL'])*1.1],
            ),
            yaxis2=dict(
                dtick=5000,
                range=[0, max(dfv['TOTAL'])*1.1],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
            )
        )

    fig.update_layout(title='Venta neta FWD USDCLP')
    fig.update_layout(legend={'itemsizing': 'constant'})
    return fig


def patrimonio_ajustado(df_vf, df_q, usdclp, total):
    fig = go.Figure()

    AFPs = df_q['AFP'].unique()
    Qs = list()
    for afp in AFPs:
        Q_afp = df_q[df_q['AFP'] == afp].reset_index()
        VF_afp = df_vf[df_vf['AFP'] == afp].reset_index()

        last_date = max(Q_afp['Fecha'])
        # / df_vf[df_vf['Fecha'] == last_date]['VF_A'].squeeze()
        Q_afp['Q_A'] = VF_afp['VF_A'] / Q_afp['Q_A'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_A'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_B'].squeeze()
        Q_afp['Q_B'] = VF_afp['VF_B'] / Q_afp['Q_B'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_B'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_C'].squeeze()
        Q_afp['Q_C'] = VF_afp['VF_C'] / Q_afp['Q_C'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_C'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_D'].squeeze()
        Q_afp['Q_D'] = VF_afp['VF_D'] / Q_afp['Q_D'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_D'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_E'].squeeze()
        Q_afp['Q_E'] = VF_afp['VF_E'] / Q_afp['Q_E'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_E'].squeeze()
        Qs.append(Q_afp)

    df_q = pd.concat(Qs)
    df_q = df_q.drop(columns=['AFP']).groupby(['Fecha']).sum().reset_index()

    last_fx = max(usdclp['Fecha'])
    df_q['Q_A'] = df_q['Q_A'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_B'] = df_q['Q_B'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_C'] = df_q['Q_C'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_D'] = df_q['Q_D'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_E'] = df_q['Q_E'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()

    if total:
        y_q = df_q['Q_A'] + df_q['Q_B'] + \
            df_q['Q_C'] + df_q['Q_D'] + df_q['Q_E']
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=y_q,
                                 yaxis="y", marker_color='royalblue', name='Total Fondos', hovertemplate='%{x}, %{y:.1f}'))

        fig.update_layout(title='Total Patrimonio Ajustado por Rentabilidad')
        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[min(y_q)*0.99, max(y_q)*1.01],
            ),
            yaxis2=dict(
                range=[min(y_q)*0.99, max(y_q)*1.01],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
            )
        )
    else:
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_A'],
                                 yaxis="y",  marker_color='royalblue', name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_B'],
                                 yaxis="y", name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_C'],
                                 yaxis="y", name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_D'],
                                 yaxis="y", name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_E'],
                                 yaxis="y", name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))
        fig.update_layout(
            title='Patrimonio del Fondo Ajustado por Rentabilidad')
        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[min(df_q['Q_A'])*0.95, max(df_q['Q_C'])*1.1],
            ),
            yaxis2=dict(
                range=[min(df_q['Q_A'])*0.95, max(df_q['Q_C'])*1.1],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
            )
        )
    fig.update_layout(yaxis={'title': "USD"})

    return fig


def clp_to_usd(df, usdclp):
    # print(usdclp.columns)
    # usdclp['Fecha'] = usdclp['Fecha'].str.slice(stop=10)
    df_new = df.copy().reset_index()

    usdclp['Fecha'] = pd.to_datetime(usdclp['Fecha'])
    df_new['Fecha'] = pd.to_datetime(df_new['Fecha'])

    for i in range(len(df_new)):
        fx = usdclp[usdclp['Fecha'] == df_new.loc[i, 'Fecha']]['Precio']
        if fx is not None and len(fx) > 0:
            # print(df.loc[i,'VF_A'] )
            # print(fx.squeeze())
            # print(df.loc[i,'Fecha'], ": ", df.loc[i,'VF_A'], "/", fx)
            df_new.loc[i, 'VF_A'] = df_new.loc[i, 'VF_A'] / fx.squeeze()
            df_new.loc[i, 'VF_B'] = df_new.loc[i, 'VF_B'] / fx.squeeze()
            df_new.loc[i, 'VF_C'] = df_new.loc[i, 'VF_C'] / fx.squeeze()
            df_new.loc[i, 'VF_D'] = df_new.loc[i, 'VF_D'] / fx.squeeze()
            df_new.loc[i, 'VF_E'] = df_new.loc[i, 'VF_E'] / fx.squeeze()
        else:
            j = i - 1
            flag = False
            while (j > 0):
                fx = usdclp[usdclp['Fecha'] ==
                            df_new.loc[j, 'Fecha']]['Precio']

                if fx is not None and len(fx) > 0:
                    df_new.loc[i, 'VF_A'] = df_new.loc[i,
                                                       'VF_A'] / fx.squeeze()
                    df_new.loc[i, 'VF_B'] = df_new.loc[i,
                                                       'VF_B'] / fx.squeeze()
                    df_new.loc[i, 'VF_C'] = df_new.loc[i,
                                                       'VF_C'] / fx.squeeze()
                    df_new.loc[i, 'VF_D'] = df_new.loc[i,
                                                       'VF_D'] / fx.squeeze()
                    df_new.loc[i, 'VF_E'] = df_new.loc[i,
                                                       'VF_E'] / fx.squeeze()
                    flag = True
                    j = -9
                    break
                j = j - 1

            if not flag:
                df_new.loc[i, 'VF_A'] = df_new.loc[i, 'VF_A'] / 820
                df_new.loc[i, 'VF_B'] = df_new.loc[i, 'VF_B'] / 820
                df_new.loc[i, 'VF_C'] = df_new.loc[i, 'VF_C'] / 820
                df_new.loc[i, 'VF_D'] = df_new.loc[i, 'VF_D'] / 820
                df_new.loc[i, 'VF_E'] = df_new.loc[i, 'VF_E'] / 820

    return df_new


def fig_afp(df_vf, usdclp):
    df_vf = df_vf.drop(columns='AFP', inplace=False).groupby(
        ['Fecha']).sum().reset_index()
    df_vf = clp_to_usd(df_vf, usdclp)
    fig = go.Figure()

    # fondos
    fig.add_trace(go.Scatter(
        x=df_vf['Fecha'], y=df_vf['VF_A'], name='Patrimonio Fondo A', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_vf['Fecha'], y=df_vf['VF_B'], name='Patrimonio Fondo B', hovertemplate='%{x}, %{y:.1f}', visible="legendonly"))
    fig.add_trace(go.Scatter(
        x=df_vf['Fecha'], y=df_vf['VF_C'], name='Patrimonio Fondo C', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_vf['Fecha'], y=df_vf['VF_D'], name='Patrimonio Fondo D', hovertemplate='%{x}, %{y:.1f}', visible="legendonly"))
    fig.add_trace(go.Scatter(
        x=df_vf['Fecha'], y=df_vf['VF_E'], name='Patrimonio Fondo E', hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': "USD"},
                      title="Patrimonio Fondos de Pensiones")

    return fig


def fig_forwards_nacional_afp(dfc, dfv, df, usdclp, df_vf, df_q):

    dif = dif_forward_nacional(dfc, dfv, df)

    color = np.array(['rgb(255,255,255)']*dif['Dif'].shape[0])
    color[dif['Dif'] < 0] = 'red'
    color[dif['Dif'] >= 0] = 'green'

    hover = list()
    for i in dif['Dif']:
        if i >= 0:
            hover.append('▲ UP: ' + str(round(i, 2)))
        else:
            hover.append('▼ DOWN: ' + str(round(i, 2)))

    fig = go.Figure()
    # forwards
    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'], yaxis="y",
                             name='Pos Neta Fwd (Vendida)', marker_color='RoyalBlue', hovertemplate='%{x}, %{y:.1f}'))

    fig.add_trace(go.Bar(
        name='Cambio en Pos Neta Fwd',
        x=dif['Fecha'],
        y=dif['Dif'].abs(),
        marker=dict(color=color.tolist()),
        hovertext=hover
    ))

    fig.add_trace(go.Scatter(x=dfc['Fecha'], y=dfc['TOTAL'].abs(
    ), yaxis="y", name='Pos Comprada Fwd', marker_color='red', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=dfv['Fecha'], y=dfv['TOTAL'], yaxis="y",
                             name='Pos Vendida Fwd', marker_color='green', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=usdclp['Fecha'], y=usdclp['Precio'], yaxis="y4",
                             name='USD/CLP', marker_color='orange', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))

    # fondos
    df_vf_usd = df_vf.drop(columns='AFP', inplace=False).groupby(
        ['Fecha']).sum().reset_index()
    df_vf_usd = clp_to_usd(df_vf_usd, usdclp)

    fig.add_trace(go.Scatter(x=df_vf_usd['Fecha'], y=df_vf_usd['VF_A'],
                             yaxis="y2", name='Patrimonio Fondo A', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_vf_usd['Fecha'], y=df_vf_usd['VF_B'],
                             yaxis="y2", name='Patrimonio Fondo B', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_vf_usd['Fecha'], y=df_vf_usd['VF_C'],
                             yaxis="y2", name='Patrimonio Fondo C', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_vf_usd['Fecha'], y=df_vf_usd['VF_D'],
                             yaxis="y2", name='Patrimonio Fondo D', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_vf_usd['Fecha'], y=df_vf_usd['VF_E'],
                             yaxis="y2", name='Patrimonio Fondo E', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))

    AFPs = df_q['AFP'].unique()
    Qs = list()
    for afp in AFPs:
        Q_afp = df_q[df_q['AFP'] == afp].reset_index()
        VF_afp = df_vf[df_vf['AFP'] == afp].reset_index()

        last_date = max(Q_afp['Fecha'])
        # / df_vf[df_vf['Fecha'] == last_date]['VF_A'].squeeze()
        Q_afp['Q_A'] = VF_afp['VF_A'] / Q_afp['Q_A'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_A'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_B'].squeeze()
        Q_afp['Q_B'] = VF_afp['VF_B'] / Q_afp['Q_B'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_B'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_C'].squeeze()
        Q_afp['Q_C'] = VF_afp['VF_C'] / Q_afp['Q_C'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_C'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_D'].squeeze()
        Q_afp['Q_D'] = VF_afp['VF_D'] / Q_afp['Q_D'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_D'].squeeze()
        # / df_vf[df_vf['Fecha'] == last_date]['VF_E'].squeeze()
        Q_afp['Q_E'] = VF_afp['VF_E'] / Q_afp['Q_E'] * \
            Q_afp[Q_afp['Fecha'] == last_date]['Q_E'].squeeze()
        Qs.append(Q_afp)

    df_q = pd.concat(Qs)
    df_q = df_q.drop(columns=['AFP']).groupby(['Fecha']).sum().reset_index()

    last_fx = max(usdclp['Fecha'])
    df_q['Q_A'] = df_q['Q_A'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_B'] = df_q['Q_B'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_C'] = df_q['Q_C'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_D'] = df_q['Q_D'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()
    df_q['Q_E'] = df_q['Q_E'] / \
        usdclp[usdclp['Fecha'] == last_fx]['Precio'].squeeze()

    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_A'],
                             yaxis="y3", name='Cambios de Fondo A', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_B'],
                             yaxis="y3", name='Cambios de Fondo B', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_C'],
                             yaxis="y3", name='Cambios de Fondo C', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_D'],
                             yaxis="y3", name='Cambios de Fondo D', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(x=df_q['Fecha'], y=df_q['Q_E'],
                             yaxis="y3", name='Cambios de Fondo E', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))

    # Create axis objects
    fig.update_layout(
        xaxis=dict(
            domain=[0.1, 0.8]
        ),
        yaxis=dict(
            title="Forwards MMUSD",
            titlefont=dict(
                color="RoyalBlue"
            ),
            tickfont=dict(
                color="RoyalBlue"
            ),
            position=0,
            dtick=5000
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

    fig.update_layout(title='Venta neta FWD USDCLP AFP')

    return fig


def fig_total_ex_fwd(df_ex, dfc, dfv, df):
    fig = go.Figure()

    dif = dif_forward_nacional(dfc, dfv, df)

    fig.add_trace(go.Scatter(x=dif['Fecha'], y=dif['TOTAL'],
                             name='Pos Neta Fwd (Vendida)', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_ex['Fecha'], y=df_ex['MMUSD_TOTAL'], name='Total', hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': 'MMUSD'},
                      title='INVERSIÓN EXTRANJERA TOTAL MMUSD')
    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))

    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, max(df_ex['MMUSD_TOTAL'])*1.1],
        ),
        yaxis2=dict(
            range=[0, max(df_ex['MMUSD_TOTAL'])*1.1],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
        )
    )
    return fig


def fig_inversiones(df_input, label, tipo):
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

    if label != 'INVERSIÓN EXTRANJERA':
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[t+'TOTAL'], name='Total', hovertemplate='%{x}, %{y:.1f}'))
        top = max([max(df[t+'A']), max(df[t+'B']), max(df[t+'C']),
                   max(df[t+'D']), max(df[t+'E']), max(df[t+'TOTAL'])])
    else:
        top = max([max(df[t+'A']), max(df[t+'B']), max(df[t+'C']),
                   max(df[t+'D']), max(df[t+'E'])])

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df[t+'A'], name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df[t+'B'], name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df[t+'C'], name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df[t+'D'], name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df[t+'E'], name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': y_title},
                      title=title)
    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))

    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, top*1.05],
        ),
        yaxis2=dict(
            range=[0, top*1.05],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
        )
    )
    return fig


def fig_activos(df_input, label, tipo):
    fig = go.Figure()

    df = df_input[df_input['Nombre'] == label]
    if tipo == 'porcentaje':
        tipo = 'Porcentaje_'
        y_title = '%Fondo'
        title = label + ' Porcentaje'

        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'TOTAL'], name='Total', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'A'], name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'B'], name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'C'], name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'D'], name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo+'E'], name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))

        mini = min([min(df[tipo+'TOTAL']), min(df[tipo+'A']), min(df[tipo+'B']),
                    min(df[tipo+'C']), min(df[tipo+'D']), min(df[tipo+'E'])])-2
        topi = max([max(df[tipo+'TOTAL']), max(df[tipo+'A']), max(df[tipo+'B']),
                    max(df[tipo+'C']), max(df[tipo+'D']), max(df[tipo+'E'])])+2

        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[max(-1, mini), min(100, topi)],
            ),
            yaxis2=dict(
                range=[max(-1, mini), min(100, topi)],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
            )
        )
    else:
        y_title = tipo
        title = label + ' ' + tipo

        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[tipo], name=tipo, hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': y_title},
                      title='Activos: ' + title)
    return fig


def fig_extranjeros(df):
    fig = go.Figure()

    columns = list(df.columns)
    columns = [i for i in columns if i != 'Nombre' and i != 'Fecha']
    for label in columns[1:]:
        fig.add_trace(go.Scatter(
            x=df['Fecha'], y=df[label], name=label, hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': 'Extranjeros'},
                      title='Activos: ' + 'MMUSD')
    return fig


def fig_hedge(df_inter, dfc, dfv, df_fn, usdclp, resumen=False):
    df_fn = dif_forward_nacional(dfc, dfv, df_fn).reset_index()

    fig = go.Figure()

    df_inter = df_inter[df_inter['Nombre'] ==
                        'INVERSIÓN EXTRANJERA'].reset_index()

    fig.add_trace(go.Scatter(
        x=df_fn['Fecha'], y=df_fn['Fondo_A']/df_inter['MMUSD_A']*100, yaxis="y", name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_fn['Fecha'], y=df_fn['Fondo_B']/df_inter['MMUSD_B']*100, yaxis="y", name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_fn['Fecha'], y=df_fn['Fondo_C']/df_inter['MMUSD_C']*100, yaxis="y", name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_fn['Fecha'], y=df_fn['Fondo_D']/df_inter['MMUSD_D']*100, yaxis="y", name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df_fn['Fecha'], y=df_fn['Fondo_E']/df_inter['MMUSD_E']*100, yaxis="y", name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))

    if not resumen:
        fig.add_trace(go.Scatter(x=usdclp['Fecha'], y=usdclp['Precio'], yaxis="y2",
                                 name='USD/CLP', marker_color='orange', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
        # Create axis objects
        fig.update_layout(
            xaxis=dict(
                domain=[0.1, 1]
            ),
            yaxis=dict(
                title="%Fondo",
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

    else:
        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[0, 100],
                tickmode='array',
                tickvals=[i*10 for i in range(11)],
            ),
            yaxis2=dict(
                range=[0, 100],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
                tickmode='array',
                tickvals=[i*10 for i in range(11)],
            )
        )
    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Porcentaje Inversión Extranjera Hedge')

    return fig


def fig_hedge_total(df_inter, dfc, dfv, df_fn, usdclp, resumen=False):
    df_fn = dif_forward_nacional(dfc, dfv, df_fn).reset_index()
    fig = go.Figure()

    df_inter = df_inter[df_inter['Nombre'] ==
                        'INVERSIÓN EXTRANJERA'].reset_index()

    y_p = df_fn['TOTAL']/df_inter['MMUSD_TOTAL']*100
    fig.add_trace(go.Scatter(
        x=df_inter['Fecha'], y=y_p, yaxis="y", name='Total', hovertemplate='%{x}, %{y:.1f}'))

    if not resumen:
        fig.add_trace(go.Scatter(x=usdclp['Fecha'], y=usdclp['Precio'], yaxis="y2",
                                 name='USD/CLP', marker_color='orange', visible="legendonly", hovertemplate='%{x}, %{y:.1f}'))
        # Create axis objects
        fig.update_layout(
            xaxis=dict(
                domain=[0.1, 1]
            ),
            yaxis=dict(
                title="%Fondo",
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
    else:
        fig.add_trace(go.Scatter(
            x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
        fig.update_layout(
            xaxis=dict(domain=[0, 0.985]),
            yaxis=dict(
                range=[max(0, min(y_p)-2), min(100, max(y_p)+2)],
            ),
            yaxis2=dict(
                range=[max(0, min(y_p)-2), min(100, max(y_p)+2)],
                position=0.985,
                anchor="x",
                overlaying="y",
                side="right",
            )
        )

    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Porcentaje Inversión Extranjera Hedge TOTAL')

    return fig


def fig_valor_fondos(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['VF_A'], name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['VF_B'], name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['VF_C'], name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['VF_D'], name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['VF_E'], name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': 'F Index'},
                      title='Fondos AFP: F Index')
    return fig


def fig_q_index(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Q_A'], name='Fondo A', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Q_B'], name='Fondo B', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Q_C'], name='Fondo C', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Q_D'], name='Fondo D', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Q_E'], name='Fondo E', hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': 'U Index'},
                      title='Fondos AFP: U Index')
    return fig


def bar_inversion_nacional(df_nacio, fondo):
    fig = go.Figure()
    fechas = pd.to_datetime(df_nacio.Fecha.unique())
    y_rv = list()
    y_instr = list()
    y_bb = list()
    y_dp = list()
    y_otros = list()

    for i in fechas:
        rv = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'RENTA VARIABLE')]['Porcentaje_'+fondo]

        y_rv.append(float(rv.squeeze()))

        instr = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'Instrumentos')]['Porcentaje_'+fondo]

        y_instr.append(float(instr.squeeze()))

        bb = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'Bonos Bancarios')]['Porcentaje_'+fondo]
        y_bb.append(float(bb.squeeze()))

        dp = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'Depósitos a Plazo')]['Porcentaje_'+fondo]
        y_dp.append(float(dp.squeeze()))

        rf = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'RENTA FIJA')]['Porcentaje_'+fondo]
        otros = float(rf.squeeze()) - float(instr.squeeze()) - \
            float(bb.squeeze()) - float(dp.squeeze())
        y_otros.append(otros)

    fig.add_trace(
        go.Bar(x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_otros, name='RF: Otros'))
    fig.add_trace(go.Bar(
        x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_dp, name='RF: Depósitos a Plazo'))
    fig.add_trace(go.Bar(
        x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_bb, name='RF: Bonos Bancarios'))
    fig.add_trace(go.Bar(
        x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_instr, name='RF: Bonos Tesorería'))
    fig.add_trace(
        go.Bar(x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_rv, name='Renta Variable'))

    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Inversión Nacional ' + fondo)

    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, 100],
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        ),
        yaxis2=dict(
            range=[0, 100],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        )
    )

    fig.update_layout(barmode='stack')
    return fig


def bar_inversion_nacional_monedas(df_bonos_clp, df_bonos_uf, fondo):
    fig = go.Figure()
    fechas = pd.to_datetime(df_bonos_clp.Fecha.unique())
    df_bonos_clp['Porcentaje_'+fondo]
    fig.add_trace(go.Bar(
        x=fechas, y=df_bonos_clp['Porcentaje_'+fondo], name='Bonos CLP', hovertemplate='%{x}, %{y:.1f}'))
    fig.add_trace(go.Bar(
        x=fechas, y=df_bonos_uf['Porcentaje_'+fondo], name='Bonos UF', hovertemplate='%{x}, %{y:.1f}'))
    # promedio
    promedio_clp = sum(df_bonos_clp['Porcentaje_'+fondo]) / \
        len(df_bonos_clp['Porcentaje_'+fondo])
    fig.add_shape(
        # Line Horizontal
        go.layout.Shape(
            type="line",
            x0=fechas[0],
            y0=promedio_clp,
            x1=fechas[-1],
            y1=promedio_clp,
            line=dict(
                color='black',
                width=2,
                dash="dashdot",
            ),
        ))

    fig.add_trace(go.Scatter(x=[fechas[0], fechas[-1]],
                             y=[promedio_clp, promedio_clp],
                             name='Promedio CLP: ' +
                             str(int(promedio_clp))+'%',
                             mode='markers',
                             marker=dict(color=['black']),
                             hovertemplate='%{x}, %{y:.1f}'))
    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Inversión Nacional Bonos ' + fondo)
    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))

    top = max(df_bonos_clp['Porcentaje_'+fondo] +
              df_bonos_clp['Porcentaje_'+fondo]) + 10

    if top > 50:
        step = 10
    else:
        step = 5

    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, min(100, top)],
            dtick=step
        ),
        yaxis2=dict(
            range=[0, min(100, top)],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
            dtick=step
        )
    )
    fig.update_layout(barmode='stack')
    return fig


def bar_inversion_internacional(df_inter, fondo):
    fig = go.Figure()
    fechas = pd.to_datetime(df_inter.Fecha.unique())
    y_rv = list()
    y_rf = list()
    for i in fechas:
        rv = df_inter[(df_inter['Fecha'] == i) & (
            df_inter['Nombre'] == 'RENTA VARIABLE')]['Porcentaje_'+fondo]
        y_rv.append(float(rv))

        rf = df_inter[(df_inter['Fecha'] == i) & (
            df_inter['Nombre'] == 'RENTA FIJA')]['Porcentaje_'+fondo]
        y_rf.append(float(rf))

    fig.add_trace(
        go.Bar(x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_rv, name='Renta Variable'))
    fig.add_trace(
        go.Bar(x=fechas, hovertemplate='%{x}, %{y:.1f}', y=y_rf, name='Renta Fija'))

    # promedio
    if len(y_rv) != 0:
        promedio_rv = sum(y_rv)/len(y_rv)
        fig.add_shape(
            # Line Horizontal
            go.layout.Shape(
                type="line",
                x0=fechas[0],
                y0=promedio_rv,
                x1=fechas[-1],
                y1=promedio_rv,
                line=dict(
                    color='black',
                    width=2,
                    dash="dashdot",
                ),
            ))

    fig.add_trace(go.Scatter(x=[fechas[0], fechas[-1]],
                             y=[promedio_rv, promedio_rv],
                             name='Promedio RV: ' +
                             str(int(promedio_rv))+'%',
                             mode='markers',
                             marker=dict(color=['black']),
                             hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Inversión Internacional ' + fondo)
    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, 100],
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        ),
        yaxis2=dict(
            range=[0, 100],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        )
    )
    fig.update_layout(barmode='stack')
    return fig


def bar_inversion(df_nacio, df_inter, fondo):
    fig = go.Figure()
    fechas = pd.to_datetime(df_nacio.Fecha.unique())
    y_nacio = list()
    y_inter = list()
    for i in fechas:
        nacio = df_nacio[(df_nacio['Fecha'] == i) & (
            df_nacio['Nombre'] == 'INVERSIÓN NACIONAL TOTAL')]['Porcentaje_'+fondo]
        y_nacio.append(float(nacio))

        inter = df_inter[(df_inter['Fecha'] == i) & (
            df_inter['Nombre'] == 'INVERSIÓN EXTRANJERA')]['Porcentaje_'+fondo]
        y_inter.append(float(inter))

    fig.add_trace(go.Bar(x=fechas, y=y_nacio, name='Nacional',
                         hovertemplate='%{x}, %{y:.1f}',))
    fig.add_trace(go.Bar(x=fechas, y=y_inter,
                         name='Internacional', hovertemplate='%{x}, %{y:.1f}'))

    # promedio
    if len(y_nacio) != 0:
        promedio_nacional = sum(y_nacio)/len(y_nacio)
        fig.add_shape(
            # Line Horizontal
            go.layout.Shape(
                type="line",
                x0=fechas[0],
                y0=promedio_nacional,
                x1=fechas[-1],
                y1=promedio_nacional,
                line=dict(
                    color='black',
                    width=2,
                    dash="dashdot",
                ),
            ))

    fig.add_trace(go.Scatter(x=[fechas[0], fechas[-1]],
                             y=[promedio_nacional, promedio_nacional],
                             name='Promedio Nacional: ' +
                             str(int(promedio_nacional))+'%',
                             mode='markers',
                             marker=dict(color=['black']),
                             hovertemplate='%{x}, %{y:.1f}'))

    fig.update_layout(yaxis={'title': '%Fondo'},
                      title='Inversión ' + fondo)

    fig.add_trace(go.Scatter(
        x=[0], y=[0], visible=False, showlegend=False, yaxis="y2"))
    fig.update_layout(
        xaxis=dict(domain=[0, 0.985]),
        yaxis=dict(
            range=[0, 100],
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        ),
        yaxis2=dict(
            range=[0, 100],
            position=0.985,
            anchor="x",
            overlaying="y",
            side="right",
            tickmode='array',
            tickvals=[i*10 for i in range(11)],
        )
    )
    fig.update_layout(barmode='stack')
    return fig
