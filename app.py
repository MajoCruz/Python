import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import yfinance as yf
import datetime
import pandas as pd
import pyfolio as pf
import warnings
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import math

stocks=["BN.PA", "KO", "MDLZ","MMC", "NESN.SW", "PEP"]
end= datetime.datetime.now()
start= end - datetime.timedelta(days=365*3)

data= yf.download(stocks, start=start, end=end)["Adj Close"].dropna()

#construir dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server


app.title="Dashboard"


app.layout = html.Div([
    html.H1("ACCIONES EMPRESAS DE CONSUMO MASIVO"),

    dcc.Dropdown(
        id='Acciones',
        options=[{'label': accion, 'value': accion} for accion in stocks],
        multi=True,
        value=['KO',"NESN.SW"],  
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='Indicador',
        options=[
            {'label': 'Precio', 'value': 'precio'},
            {'label': 'Rendimiento Acumulado', 'value': 'rendimiento'}
        ],
        value='precio',
        style={'width': '50%'}
    ),

   dcc.RangeSlider(
    id='Periodo',
    marks={i:  (start + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, 365 * 3, 200)},
    min=0,
    max=365 * 3, 
    step=30,
    value=[0, 365 * 3]
),

    dcc.Graph(id='Grafica de lineas'),
])

@app.callback(
    Output('Grafica de lineas', 'figure'),
    [Input('Acciones', 'value'),
     Input('Indicador', 'value'),
     Input('Periodo', 'value')]
)
def actualizar_grafico(acciones, selector, fechas):
    if selector == "precio":
        df_filtered = data[acciones].iloc[fechas[0]:fechas[1]]
    elif selector == "rendimiento":
        df_filtered = (1 + data[acciones].pct_change()).cumprod().iloc[fechas[0]:fechas[1]]
    else:
        df_filtered = pd.DataFrame()  # Maneja otras opciones aquí

    fig = px.line(df_filtered, x=df_filtered.index, y=df_filtered.columns, labels={'value': selector},
                  title=f'{selector} de {",  ".join(acciones)}')

    return fig

#setear server y correr
if__name__=="__main__"
app.run_server(debug=False,host ="0.0.0.0", port=10002)
