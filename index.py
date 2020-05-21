import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server
from layouts import layout_fn,layout_activos, layout_extranjeros, layout_home, layout_internacional, layout_nacional#layout_afp,
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout_home
    elif pathname == '/apps/forwards-nacionales':
        return layout_fn
    elif pathname == '/apps/inversion-nacional':
        return layout_nacional
    elif pathname == '/apps/inversion-internacional':
        return layout_internacional
    elif pathname == '/apps/activos':
        return layout_activos
    elif pathname == '/apps/extranjeros':
        return layout_extranjeros
    #elif pathname == '/apps/valores':
    #    return layout_afp
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)