
from datetime import datetime
import dash

from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash,dcc,html,Input,Output
import time

df= pd.read_excel("inflacion.xlsx")
df5 = pd.read_excel("IMAE.xlsx")
df8 = pd.read_excel("Ingreso por Exportaciones.xlsx")

#construir dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.title="Dashboard"

cuentas=["Inflacion"]
cuentas2=["Indice"]
cuentas3=["Azucar","Banano","Cafe","Cardamomo"]

#layout del app con graficas
app.layout = html.Div([
    html.Div([html.Div([
    
    #Inflacion
    html.Div(dcc.Dropdown(
    id="Inflacion_año",value=["2019","2020","2021","2022","2023"],clearable=False, multi=True,
    options=[{'label':x,'value':x} for x in sorted(df.Año.unique())]
    ),className="six columns", style={"width":"50%"},),
        
    html.Div(dcc.Dropdown(
    id="Inflacion_total",value="Inflacion",clearable=False,
    options=[{'label':x,'value':x} for x in cuentas]), className="six columns"),
    
    html.Div([dcc.Graph(id="graph",figure={},config={"displayModeBar":True,"displaylogo":False,
                                                    }),],style={'width':'1100px'}),
    
    html.Div([dcc.Graph(id="boxplot",figure={},)],style={"width":'1100px'}),
    
    html.Div(html.Div(id="table-container"),style={'marginBottom':'15px','marginTop':
                                                 "10px"}),
    html.Div(dcc.Dropdown(
    id="Indice_año",value=["2018","2019","2020","2021","2022","2023"],clearable=False, multi=True,
    options=[{'label':x,'value':x} for x in sorted(df.Año.unique())]
    ),className="six columns", style={"width":"50%"},),
    
    #IMAEA
    html.Div(dcc.Dropdown(
    id="Indice",value="Indice",clearable=False,
    options=[{'label':x,'value':x} for x in cuentas2]), className="six columns"), 

    html.Div([dcc.Graph(id="graph1",figure={},config={"displayModeBar":True,"displaylogo":False,
                                                    }),],style={'width':'1100px'}),
    
    html.Div([dcc.Graph(id="boxplot1",figure={},)],style={"width":'1100px'}),
    
    html.Div(html.Div(id="table-container1"),style={'marginBottom':'15px','marginTop':
                                                 "10px"}),
    
    #Ingreso por exportacion
    html.Div(dcc.Dropdown(
    id="Ingreso_año",value=["2017","2018","2019","2020","2021","2022","2023"],clearable=False, multi=True,
    options=[{'label':x,'value':x} for x in sorted(df.Año.unique())]
    ),className="six columns", style={"width":"50%"},),
    
    html.Div(dcc.Dropdown(
    id="Ingreso_productos",value=["Azucar","Banano","Cafe","Cardamomo"],clearable=False,
    options=[{'label':x,'value':x} for x in cuentas3]), className="six columns"), 
    ], className="row"),],className="custom-dropdown"),
    
    html.Div([dcc.Graph(id="graph2",figure={},config={"displayModeBar":True,"displaylogo":False,

                                                    }),],style={'width':'1100px'}),
    html.Div([dcc.Graph(id="boxplot2",figure={},)],style={"width":'1100px'}),
    
    html.Div(html.Div(id="table-container2"),style={'marginBottom':'15px','marginTop':
                                                 "10px"}),])

#callback de la funcion
@app.callback(
    [Output(component_id="graph",component_property="figure"),
    Output(component_id="boxplot",component_property="figure"),
    Output("table-container",'children')],
    [Input(component_id="Inflacion_año",component_property="value"),
    Input(component_id="Inflacion_total",component_property="value")]
)
def display_value(selected_año,selected_mes):
    if len(selected_año)==0:
        df2=df[df["Año"].isin(["2019","2020","2021","2022","2023"])]
    else:
        df2=df[df["Año"].isin(selected_año)]
    
    #grafica lineas
    fig= px.line(df2,color="Año",x="Mes",markers=True,y=selected_mes,
                width=1000,height=500)
    
    fig.update_layout(title=f'{selected_mes} de {selected_año}',
                     xaxis_title="Inflacion Mensual",)
    fig.update_traces(line=dict(width=2))
    
    #grafica box plot
    fig2=px.box(df2,color="Año",x="Año",y=selected_mes,
               width=1000,height=500)
    fig2.update_layout(title=f'{selected_mes} de {selected_año}',
                      )
    
    #modificar data frame para poder hacerlo tabla
    df_reshaped = df2.pivot(index='Año', columns='Mes', values=selected_mes)
    df_reshaped_3 = df_reshaped.reset_index()

    #tabla
    return (fig,fig2,
           dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped_3],
                               data=df_reshaped_3.to_dict("records"),
                               export_format="csv",#para guardar como csv
                               fill_width=True,
                               style_header={'backgroundColor':'blue',
                                            'color':'white'},
                               ))

@app.callback(
    [Output(component_id="graph1",component_property="figure"),
    Output(component_id="boxplot1",component_property="figure"),
    Output("table-container1",'children')],
    [Input(component_id="Indice_año",component_property="value"),
    Input(component_id="Indice",component_property="value")]
)

#definicion de la funcion

def display_value(selected_año,selected_mes):
    if len(selected_año)==0:
        df6=df5[df5["Año"].isin(["2018","2019","2020","2021","2022","2023"])]
    else:
        df6=df5[df5["Año"].isin(selected_año)]
    
    #grafica lineas
    fig= px.line(df6,color="Año",x="Mes",markers=True,y=selected_mes,
                width=1000,height=500)
    
    fig.update_layout(title=f'{selected_mes} de {selected_año}',
                     xaxis_title="Indice Mensual",)
    fig.update_traces(line=dict(width=2))
    
    #grafica boxplot
    fig2=px.box(df6,color="Año",x="Año",y=selected_mes,
               width=1000,height=500)
    fig2.update_layout(title=f'{selected_mes} de {selected_año}',
                      )
    
    #modificar data frame para poder hacerlo tabla
    df_reshaped = df6.pivot(index='Año', columns='Mes', values=selected_mes)
    df_reshaped_4 = df_reshaped.reset_index()

    #tabla
    return (fig,fig2,
           dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped_4],
                               data=df_reshaped_4.to_dict("records"),
                               export_format="csv",#para guardar como csv
                               fill_width=True,
                               style_header={'backgroundColor':'blue',
                                            'color':'white'},
                               ))

@app.callback(
    [Output(component_id="graph2",component_property="figure"),
    Output(component_id="boxplot2",component_property="figure"),
    Output("table-container2",'children')],
    [Input(component_id="Ingreso_año",component_property="value"),
    Input(component_id="Ingreso_productos",component_property="value")]
)

#definicion de la funcion

def display_value(selected_uno,selected_dos):
    if len(selected_uno)==0:
        df9=df8[df8["Año"].isin(["2017","2018","2019","2020","2021","2022","2023"])]
    else:
        df9=df8[df8["Año"].isin(selected_uno)]
    
    #grafica1
    fig6= px.line(df9,color="Año",x="Mes",markers=True,y=selected_dos,
                width=1000,height=500)
    
    fig6.update_layout(title=f'{selected_dos} de {selected_uno}',
                     xaxis_title="Indice Mensual",)
    fig6.update_traces(line=dict(width=2))
    
    #grafica 2
    fig7=px.box(df9,color="Año",x="Año",y=selected_dos,
               width=1000,height=500)
    fig7.update_layout(title=f'{selected_dos} de {selected_uno}',
                      )
    
    #modificar data frame para poder hacerlo tabla
    df_reshaped = df9.pivot(index='Año', columns='Mes', values=selected_dos)
    df_reshaped_5 = df_reshaped.reset_index()

    #tabla
    return (fig6,fig7,
           dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped_5],
                               data=df_reshaped_5.to_dict("records"),
                               export_format="csv",#para guardar como csv
                               fill_width=True,
                               style_header={'backgroundColor':'blue',
                                            'color':'white'},
                               ))

#setear server y correr
app.run_server(debug=False,host ="0.0.0.0", port=10000)
