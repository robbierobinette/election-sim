import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button('Click here to see the content', id='button'),
    html.Div(id='body-div')
])

count = 0

@app.callback(
    Output(component_id='body-div', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')]
)
def update_output(n_clicks):
    global count
    count += 1
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Elephants are the only animal that can't jump: %d" % count


if __name__ == '__main__':
    app.run_server(debug=True)