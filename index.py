import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        from layouts.layout_home import layout_home_head
        return layout_home_head

    elif pathname == '/apps/forwards-nacionales':
        from layouts.layout_forwards import layout_datos
        return layout_datos

    elif pathname == '/apps/inversion-nacional':
        from layouts.layout_nacional import layout_nacional
        return layout_nacional

    elif pathname == '/apps/inversiones':
        from layouts.layout_inversiones import layout_inversiones
        return layout_inversiones

    elif pathname == '/apps/inversion-internacional':
        from layouts.layout_internacional import layout_internacional
        return layout_internacional

    elif pathname == '/apps/activos':
        from layouts.layout_activos import layout_activos
        return layout_activos

    elif pathname == '/apps/extranjeros':
        from layouts.layout_extranjeros import layout_extranjeros
        return layout_extranjeros
    # elif pathname == '/apps/valores':
    #    return layout_afp
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=False)
