'''
esegui lo script python3 grafici.py e poi vai su http://127.0.0.1:8052/
'''






import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash import dash_table
import pandas as pd

# connecting the page to the app.py file
dash.register_page(__name__, path='/page-1', name='Statistiche per partita')

df_luiss_giocatori=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_players_luiss.csv", sep=';')


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
            {'label': 'FGA2', 'value': '2PA_tot'},
            {'label': 'FGM2', 'value': '2PM_tot'},
            {'label': '2P%', 'value': '2P%_tot'},
            {'label': 'FGM3', 'value': '3PM_tot'},
            {'label': 'FGA3', 'value': '3PA_tot'},
            {'label': '3P%', 'value': '3P%_tot'},
            {'label': 'FTM', 'value': 'FTM_tot'},
            {'label': 'FTA', 'value': 'FTA_tot'},
            {'label': 'FT%', 'value': 'FT%_tot'},
            {'label': 'REB', 'value': 'REB_tot'},
            {'label': 'AST', 'value': 'AST_tot'},
            {'label': 'TOV', 'value': 'TOV_tot'},
            {'label': 'STL', 'value': 'STL_tot'},
            {'label': 'PTS', 'value': 'PTS_tot'}
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

    df_luiss_giocatori_copy = df_luiss_giocatori.copy()
    df_luiss_giocatori_copy['2PA_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['2PA'].transform('sum')
    df_luiss_giocatori_copy['2PM_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['2PM'].transform('sum')
    df_luiss_giocatori_copy['3PA_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['3PA'].transform('sum')
    df_luiss_giocatori_copy['3PM_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['3PM'].transform('sum')
    df_luiss_giocatori_copy['FTA_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['FTA'].transform('sum')
    df_luiss_giocatori_copy['FTM_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['FTM'].transform('sum')
    df_luiss_giocatori_copy['2P%_tot'] = df_luiss_giocatori_copy.apply(lambda row: (row['2PM_tot'] / row['2PA_tot'] * 100) if row['2PA_tot'] > 0 else 0, axis=1)
    df_luiss_giocatori_copy['3P%_tot'] = df_luiss_giocatori_copy.apply(lambda row: (row['3PM_tot'] / row['3PA_tot'] * 100) if row['3PA_tot'] > 0 else 0, axis=1)
    df_luiss_giocatori_copy['FT%_tot'] = df_luiss_giocatori_copy.apply(lambda row: (row['FTM_tot'] / row['FTA_tot'] * 100) if row['FTA_tot'] > 0 else 0, axis=1)
    df_luiss_giocatori_copy['AST_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['AST'].transform('sum')
    df_luiss_giocatori_copy['TOV_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['TOV'].transform('sum')
    df_luiss_giocatori_copy['STL_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['STL'].transform('sum')
    df_luiss_giocatori_copy['PTS_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['PTS'].transform('sum')
    df_luiss_giocatori_copy['REB_tot'] = df_luiss_giocatori_copy.groupby(['Player', 'HA', 'WL'])['REB'].transform('sum')



    # Filter the dataframe according to user input
    filtered_df = df_luiss_giocatori[(df_luiss_giocatori_copy['Player'].isin(giocatore)) & (df_luiss_giocatori_copy['HA'].isin(home_away))
                                     & (df_luiss_giocatori_copy['WL'].isin(win_lose))]
    
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


'''if __name__ == '__main__':
    app.layout = layout
    # Run on a different port if 8050 is already in use
    #app.run_server(debug=True, port=8050, host='0.0.0.0')
    app.run_server(debug=True, port=8052)'''
