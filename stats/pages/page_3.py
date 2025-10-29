import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash import dash_table
import pandas as pd

# ✅ registra la pagina (obbligatorio per multipage)
dash.register_page(__name__, path='/page-3', name='Pagina Difesa')


# importing the DF
df_match_opponents=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_match_opponent.csv", sep=';')
df_opponents=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_opponents.csv", sep=';')
df_opponents_merged = df_opponents.merge(df_match_opponents, on=['OPPONENT', 'DATA'], suffixes=('_opponent', '_match'), how='left')

# dropping cols
df_opponents_merged = df_opponents_merged.drop(columns=['WL_opponent', 'HA_opponent', 'SEASON_LEVEL_opponent', 'PIR', 'EFF', '+/-', 'No', 'Player', 'MIN', 'Best Partial'])

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
#server = app.server

mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(id='mygraph', figure={})

# Setting the dropdown menu
home_away=dcc.Checklist(
        id='checklist-items h/a',
        options=[
            {'label': 'Casa', 'value': 'H'},
            {'label': 'Trasferta', 'value': 'A'}
        ],
        value=['C'],
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

statistica=dcc.RadioItems(
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
            {'label': 'OREB', 'value': 'OREB'},
            {'label': 'DREB', 'value': 'DREB'},
            {'label': 'PTS', 'value': 'PTS'}
        ],
        value='2PA',  # Valore di default
        labelStyle={'display': 'block'}  # Mostra le opzioni come lista verticale
    )

layout = dbc.Container([
    # ======= TITOLO =======
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Analisi Per Giocatore'),
            html.P("In questa sezione è possibile vedere uno a scelta tra diverse statistiche, "
                   "filtrando per giocatore, partite vinte o perse e per partite in casa o in trasferta.")
        ]), width=12)
    ], className="mb-4"),

    # ======= FILTRI + TABELLE =======
    dbc.Row([
        # --- COLONNA SINISTRA (Filtri) ---
        dbc.Col([
            html.H5("🎛️ Filtri"),
            html.Label('Casa / Trasferta'),
            home_away,
            html.Br(),

            html.Label('W / L'),
            win_lose,
            html.Br(),

            html.Label('Statistica'),
            statistica,
            html.Br()
        ], width=3, style={'padding': '20px'}),

        # --- COLONNA DESTRA (Tabelle) ---
        dbc.Col([
            html.H5("📊 Tabelle di riepilogo"),
            dbc.Row([
                dbc.Col([
                    html.H6("Statistiche per Casa / Trasferta (HA)"),
                    dash_table.DataTable(
                        id='table_ha',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center', 'fontSize': 12},
                        page_size=20
                    )
                ], width=6),
                dbc.Col([
                    html.H6("Statistiche per Vittoria / Sconfitta (WL)"),
                    dash_table.DataTable(
                        id='table_wl',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center', 'fontSize': 12},
                        page_size=20
                    )
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H6("Statistiche per Casa / Trasferta (HA)"),
                    dash_table.DataTable(
                        id='table_ha_2',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center', 'fontSize': 12},
                        page_size=20
                    )
                ], width=6),
                dbc.Col([
                    html.H6("Statistiche per Vittoria / Sconfitta (WL)"),
                    dash_table.DataTable(
                        id='table_wl_2',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center', 'fontSize': 12},
                        page_size=20
                    )
                ], width=6)
            ])
        ], width=9)
    ], className="mb-5"),

    # ======= GRAFICO SOTTO =======
    dbc.Row([
        dbc.Col([
            html.H5("📈 Andamento Statistica Selezionata"),
            mygraph
        ], width=12)
    ]),

    # ======= SPAZIO FINALE =======
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '100px'})
        ])
    ])
], fluid=True)



# Callbacks and function definitions

@callback(
    Output('table_ha', 'data'),
    Output('table_ha', 'columns'),
    Output('table_wl', 'data'),
    Output('table_wl', 'columns'),
    Output('mygraph', 'figure'),
    Output('table_ha_2', 'data'),
    Output('table_ha_2', 'columns'),
    Output('table_wl_2', 'data'),
    Output('table_wl_2', 'columns'),
    Input('checklist-items h/a', 'value'),
    Input('checklist-items w/l', 'value'),
    Input('radio-items statistiche', 'value')
)
def update_graph(home_away, win_lose, statistica):
    print("=== Callback triggered ===")
    print("home_away:", home_away)
    print("win_lose:", win_lose)
    print("statistica:", statistica)

    # Controllo sicurezza
    if not home_away:
        home_away = ['H', 'A']
    if not win_lose:
        win_lose = ['W', 'L']

    # --- HA Table 1 ---
    df_match_opponents_melt_ha = df_match_opponents.melt(id_vars='HA', var_name='Statistica', value_name='Valore')
    df_match_opponents_pivot_ha = df_match_opponents_melt_ha.pivot(index='Statistica', columns='HA', values='Valore').reset_index()
    print("Pivot HA:", df_match_opponents_pivot_ha.shape)

    # --- WL Table 1 ---
    df_match_opponents_melt_wl = df_match_opponents.melt(id_vars='WL', var_name='Statistica', value_name='Valore')
    df_match_opponents_pivot_wl = df_match_opponents_melt_wl.pivot(index='Statistica', columns='WL', values='Valore').reset_index()
    print("Pivot WL:", df_match_opponents_pivot_wl.shape)

    # --- HA Table 2 ---
    df_opponents_melt_ha = df_opponents.melt(id_vars='HA', var_name='Statistica', value_name='Valore')
    df_opponents_pivot_ha = df_opponents_melt_ha.pivot(index='Statistica', columns='HA', values='Valore').reset_index()
    print("Pivot HA:", df_opponents_pivot_ha.shape)

    # --- WL Table 2 ---
    df_opponents_melt_wl = df_opponents.melt(id_vars='WL', var_name='Statistica', value_name='Valore')
    df_opponents_pivot_wl = df_opponents_melt_wl.pivot(index='Statistica', columns='WL', values='Valore').reset_index()
    print("Pivot WL:", df_opponents_pivot_wl.shape)

    # --- Filter for graph ---
    df_filtered = df_opponents_merged[
        df_opponents_merged['HA_match'].isin(home_away) &
        df_opponents_merged['WL_match'].isin(win_lose)
    ]
    print("Filtered rows:", len(df_filtered))
    print("Columns:", df_filtered.columns.tolist()[:10])

    # --- Build DataTable data ---
    data_ha = df_match_opponents_pivot_ha.to_dict('records')
    columns_ha = [{"name": i, "id": i} for i in df_match_opponents_pivot_ha.columns]
    data_wl = df_match_opponents_pivot_wl.to_dict('records')
    columns_wl = [{"name": i, "id": i} for i in df_match_opponents_pivot_wl.columns]

    data_ha_2 = df_opponents_pivot_ha.to_dict('records')
    columns_ha_2 = [{"name": i, "id": i} for i in df_opponents_pivot_ha.columns]
    data_wl_2 = df_opponents_pivot_wl.to_dict('records')
    columns_wl_2 = [{"name": i, "id": i} for i in df_opponents_pivot_wl.columns]



    # --- Graph ---
    if df_filtered.empty:
        fig = go.Figure()
        fig.update_layout(title="⚠️ Nessun dato disponibile per i filtri selezionati")
    else:
        if statistica not in df_filtered.columns:
            if f"{statistica}_match" in df_filtered.columns:
                statistica = f"{statistica}_match"
        fig = px.bar(df_filtered, x='OPPONENT', y=statistica, title=f"{statistica} per avversario", template='plotly_white')

    print("=== Callback completed ===")
    return data_ha, columns_ha, data_wl, columns_wl, fig, data_ha_2, columns_ha_2, data_wl_2, columns_wl_2



