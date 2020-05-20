import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout_fn, layout_inversiones, layout_activos, layout_extranjeros, layout_afp
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return 'HOME'
    elif pathname == '/apps/forwards-nacionales':
        return layout_fn
    elif pathname == '/apps/inversiones':
        return layout_inversiones
    elif pathname == '/apps/activos':
        return layout_activos
    elif pathname == '/apps/extranjeros':
        return layout_extranjeros
    elif pathname == '/apps/valores':
        return layout_afp
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)