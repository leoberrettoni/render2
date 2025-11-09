import plotly.express as px
from dash import dash_table
import pandas as pd
from pathlib import Path
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-1', name='Statistiche per partita')

ROOT = Path(__file__).resolve().parents[1]   # da pages/ risale alla cartella principale

# Percorso alla cartella data
DATA = ROOT / "data"
df_luiss_giocatori = pd.read_csv(DATA / "df_players_luiss.csv", sep=';')

#df_luiss_giocatori=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_players_luiss.csv", sep=';')


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
#server = app.server

mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})

# Setting the dropdown menu
giocatori = dcc.Dropdown(
id='giocatori',
options=[{'label': i, 'value': i} for i in df_luiss_giocatori['Player'].unique()],
value=['Alessio', 'Fala'],
multi=True,
clearable=False
)
home_away=dcc.Checklist(
id='checklist-items h/a',
options=[
{'label': 'Casa', 'value': 'H'},
{'label': 'Trasferta', 'value': 'A'}
],
value=['H'],
labelStyle={'display': 'block'}
)

win_lose=dcc.Checklist(
id='checklist-items w/l',
options=[
{'label': 'W', 'value': 'W'},
{'label': 'L', 'value': 'L'}
],
value=['W'],
labelStyle={'display': 'block'}
)

radio_item_statistica=dcc.RadioItems(
        id='radio-items statistiche',
        options=[
            {'label': 'FGA2', 'value': '2PA'},
            {'label': 'FGM2', 'value': '2PM'},
            {'label': '2P%', 'value': '2P%'},
            {'label': 'FGM3', 'value': '3PM'},
            {'label': 'FGA3', 'value': '3PA'},
            {'label': '3P%', 'value': '3P%'},
            {'label': 'FTM', 'value': 'FTM'},
            {'label': 'FTA', 'value': 'FTA'},
            {'label': 'FT%', 'value': 'FT%'},
            {'label': 'REB', 'value': 'REB'},
            {'label': 'AST', 'value': 'AST'},
            {'label': 'TOV', 'value': 'TOV'},
            {'label': 'STL', 'value': 'STL'},
            {'label': 'PTS', 'value': 'PTS'}
        ],
        value='2PA',  # Valore di default
        labelStyle={'display': 'block'}  # Mostra le opzioni come lista verticale
    )

layout = dbc.Container([
dbc.Row([
dbc.Col(html.Div([
html.H2('Analisi Per Giocatore'),
html.P("In questa sezione è possibile vedere uno a scelta tra diverse statistiche, "
"filtrando per giocatore, partite vinte o perse e per partite in casa o in trasferta.")
]), width=12)
]),

dbc.Row([
# Colonna sinistra - tutti i filtri uno sotto l'altro
dbc.Col([
html.Label('Casa/Trasferta'),
home_away,
html.Br(),
html.Label('W/L'),
win_lose,
html.Br(),
html.Label('Giocatori'),
giocatori,
html.Br(),
html.Label('Statistica'),
radio_item_statistica
], width=3, style={'padding': '20px'}),

# Colonna destra - grafico
dbc.Col([
mygraph
], width=9)
]),

dbc.Row([
dbc.Col([
html.Div(style={'height': '100px'})
])
], justify='center')
], fluid=True)



# Callbacks and function definitions

#@app.callback(
@callback(        
   Output(mygraph, 'figure'),
   [Input('checklist-items h/a', 'value'),
    Input('checklist-items w/l', 'value'),
    Input('giocatori', 'value'),
    Input('radio-items statistiche', 'value')]
)

def update_graph(home_away, win_lose, giocatore, statistica):

# Filter the dataframe according to user input
    filtered_df = df_luiss_giocatori[(df_luiss_giocatori['Player'].isin(giocatore)) & (df_luiss_giocatori['HA'].isin(home_away))
                                     & (df_luiss_giocatori['WL'].isin(win_lose))]
    
    # creating the plot
    fig = px.bar(
        filtered_df,  # Dataframe
        x='OPPONENT',  # x-axis
        y=statistica,  # y-axis
        color='Player',  # Symbol by player
        barmode="group",
        title=f"{statistica} per Giocatore durante il campionato",
        labels={statistica: statistica, 'Avversario': 'Avversario'}
    )

    fig.update_layout(
        xaxis_title="OPPONENT",
        yaxis_title=statistica,
        template='plotly_white'
    )

    return fig
