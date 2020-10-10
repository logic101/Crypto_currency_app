import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.graph_objects as go
import requests

app = dash.Dash('__name__')


def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'width': '100%', 'margin': 25, 'textAlign': 'center'})


app.layout = html.Div(children=[
    html.Div(
        className='row', children=[
            html.Div(className='four columns div-user-controls', children=[
                html.H2('Real-Time Crypto Analysis.'),
                html.P('Select your cryptocurrency from the dropdown below.'),
                html.Label('CryptoCurrency.'),
                dcc.Dropdown(
                    id='cryptop',
                    options=[
                        {'label': 'Bitcoin', 'value': 'BTC'},
                        {'label': 'Ethereum', 'value': 'ETH'},
                        {'label': 'Bitcoin Cash', 'value': 'BCH'},
                        {'label': 'Litecoin', 'value': 'LTC'},
                    ], value='BTC'
                ),
                html.Label('Time'),
                dcc.Dropdown(
                    id='time_crypto',
                    options=[
                        {'label': 'Minute', 'value': '1MIN'},
                        {'label': 'Day', 'value': '1DAY'},
                        {'label': 'Month', 'value': '6MTH'},
                        {'label': 'Year', 'value': '5YRS'}
                    ], value='1MIN'
                ),
                html.P('regans')
            ]
                     ),
            html.Div(className='eight columns div-for-charts bg-grey', children=[
                dcc.Graph(id='graph', config={'displayModeBar': False}),
                html.Div(id='bottom_panel',
                         className='row div-bottom-panel',
                         children=[
                             html.Div(className='display-inlineblock', children=[
                                 dcc.Dropdown(
                                     id='dropdown_positions',
                                     className='bottom-dropdowns',
                                     options=[
                                         {'label': 'Bitcoin', 'value': 'BTC'},
                                         {'label': 'Ethereum', 'value': 'ETH'},
                                         {'label': 'Bitcoin Cash', 'value': 'BCH'},
                                         {'label': 'Litecoin', 'value': 'LTC'}
                                     ],
                                     value='BTC',
                                     clearable=False,
                                     style={'border': '0px solid black'}
                                 )
                             ]),
                             html.Div(id='orders_table', className='row table-orders')
                         ]
                         )
            ]
                     )
        ]
    )
]

)
# Define callback to update graph


@app.callback(
    Output('graph', 'figure'),
    [Input("cryptop", "value"), Input('time_crypto', 'value')])
def update_figure(currency, time_change):
    apikey = '88BF8257-E755-46D1-B79B-231FA32B11C9'
    day = '1DAY'
    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'

    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)

    fig = go.Figure(data=[go.Candlestick(x=df.time_period_start,
                                         open=df.price_open,
                                         high=df.price_high,
                                         low=df.price_low,
                                         close=df.price_close, )]
                    )

    fig.update_layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                      template='plotly_dark',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin={'b': 15},
                      hovermode='x',
                      autosize=True,
                      title={'text': 'Cryptocurrency Prices', 'font': {'color': 'white'}, 'x': 0.5},)
    return fig
# The table


@app.callback(
    Output('orders_table', 'children'),
    [Input("dropdown_positions", "value")]
)
def update_table(currency):
    day = '1DAY'
    # currency=value
    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={day}'
    key = '88BF8257-E755-46D1-B79B-231FA32B11C9'
    headers = {'X-CoinAPI-Key': key}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    table_df = generate_table(df)
    return table_df


if __name__ == "__main__":
    app.run_server(debug=True, port=700)
