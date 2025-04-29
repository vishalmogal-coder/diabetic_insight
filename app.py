import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Load your CSV
file_path = 'diabetes_stages_europe_extended.csv'
df = pd.read_csv(file_path)

# List of columns to choose from (excluding Country)
columns = [col for col in df.columns if col != 'Country']

# Simple username and password
USERNAME = "admin"
PASSWORD = "password"

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server
app.title = "Global Diabetes Risk Insights"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/logoDCV.avif', style={'height': '80px', 'margin-bottom': '20px'}),
                html.H2("Global Diabetes Risk Insights", className="text-center mb-4"),
                html.Div(id='login-form', children=[
                    dbc.Input(id='username', type='text', placeholder='Username', className='mb-2'),
                    dbc.Input(id='password', type='password', placeholder='Password', className='mb-2'),
                    dbc.Button('Login', id='login-button', color='primary', className="d-grid gap-2"),
                    html.Div(id='login-output', className='text-danger mt-2')
                ], style={'textAlign': 'center'})
            ], style={'textAlign': 'center'})
        ], width=4)
    ], justify="center"),

    html.Div(id='dashboard', style={'display': 'none'}, children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    # html.Img(src='/assets/logoDCV.avif', style={'height': '80px', 'margin-bottom': '10px'}),
                    # html.H2("Global Diabetes Risk Insights", className="text-center mb-4"),
                ], style={'textAlign': 'center'})
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Select Metric:", className='font-weight-bold'),
                dcc.Dropdown(
                    id='column-dropdown',
                    options=[{'label': col, 'value': col} for col in columns],
                    value=columns[0]
                )
            ], width=6)
        ], justify="center", className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='heatmap', style={"height": "700px"})
            ])
        ])
    ])
], fluid=True)

# Callback for login
@app.callback(
    [Output('dashboard', 'style'),
     Output('login-form', 'style'),
     Output('login-output', 'children')],
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value')
)
def login(n_clicks, username, password):
    if n_clicks and username == USERNAME and password == PASSWORD:
        return {'display': 'block'}, {'display': 'none'}, ''
    elif n_clicks:
        return {'display': 'none'}, {'display': 'block'}, 'Invalid username or password.'
    return {'display': 'none'}, {'display': 'block'}, ''

# Callback to update the heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('column-dropdown', 'value')
)
def update_heatmap(selected_column):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=selected_column,
        color_continuous_scale="Reds",
        title=f"{selected_column} Across Countries"
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        title_x=0.5
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
