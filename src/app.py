import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from dash import dash_table

df=pd.read_excel('/Users/leo/Documents/Scouting/Real/dati/Live.xlsx')
df['Azione']=df['Azione'].replace('pr','Pick and Roll')
df['Azione']=df['Azione'].replace('pen','Penetrazione')
df['Azione']=df['Azione'].replace('us','Uscite')
df['Azione']=df['Azione'].replace('tr','Transizione')
df['Azione']=df['Azione'].replace('ds','Difesa schierata')
df['Azione']=df['Azione'].replace('iso','Isolamento')
df['Azione']=df['Azione'].replace('ro','Rimbalzo offensivo')
df['Azione']=df['Azione'].replace('cons','Consegnato')
df['Azione']=df['Azione'].replace('pb','Post Basso')


df_ppp=df.groupby(['Squadra', 'quarto']).agg({'Squadra': 'count', 'Punti realizzati': 'sum', 'Punti potenziali':'sum'}).rename(columns={'Squadra':'Possessi'}).reset_index()

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

mytitle = dcc.Markdown(children='')
mytable = dash_table.DataTable()

# Setting the dropdown menu
dropdown1 = dcc.Dropdown(
    options=[{'label': i, 'value': i} for i in df['Squadra'].unique()],
    value=['Alessio', 'Fala'],
    multi=True,
    clearable=False
)

# dropdown2 = dcc.Dropdown(
#     options=[{'label': i, 'value': i} for i in df['Partita'].unique()],
#     value=['San Cesareo'],
#     multi=True,
#     clearable=False
# )

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Mappa di tiro'),
            html.Div([
                html.P("In questa sezione è possobile visualizzare varie mappe di tiro. è possibile\
                filtrare per giocatore o per partita a seconda dell informazioni che si vogliono ottenere.")
                ])
        ]))]),
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mytable], width=12)
    ]),
    dbc.Row([
        dbc.Col([html.Label('Giocatori'), dropdown1], width=6),
        #dbc.Col([html.Label('Partita'), dropdown2], width=6)
    ], justify='left'),
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '100px'})
            ])
        ], justify='center')
], fluid=True)


# Callbacks and function definitions

@app.callback(
    Output(mytable, 'data'),
    [Input(dropdown1, 'value')]  # You can also include the second dropdown in the future
)
def update_table(squadra):
    df_filtered = df_ppp[df_ppp['Squadra'].isin(squadra)]
    df_filtered['Punti x Possesso'] = (df_filtered['Punti realizzati'] / df_filtered['Possessi']).round(2)
    df_filtered['Punti potenziali x Possesso'] = (df_filtered['Punti potenziali'] / df_filtered['Possessi']).round(2)
    
    # Convert DataFrame to dictionary for DataTable
    data = df_filtered.to_dict('records')
    return data

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True, port=8050)
