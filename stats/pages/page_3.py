import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash import dash_table
import pandas as pd
from pathlib import Path
import numpy as np
from dash.dash_table.Format import Format, Group, Scheme

# ✅ registra la pagina (obbligatorio per multipage)
dash.register_page(__name__, path='/page-3', name='Pagina Difesa')


# importing the DF
ROOT = Path(__file__).resolve().parents[1]   # da pages/ risale alla cartella principale

# Percorso alla cartella data
DATA = ROOT / "data"

# Leggi i CSV
df_match_opponents = pd.read_csv(DATA / "df_match_opponent.csv", sep=';')
df_opponents = pd.read_csv(DATA / "df_opponents.csv", sep=';')

#df_match_opponents=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_match_opponent.csv", sep=';')
#df_opponents=pd.read_csv("/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_opponents.csv", sep=';')
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




# Defining the tables to be plotted in the callback
# Setting the exclude stats
exclude_stats_ha = ["Best Partial", "OPPONENT", "WL", "SEASON_LEVEL", "DATA", "Squadra", "Bench Points", "Starter Points"]
exclude_stats_wl = ["Best Partial", "OPPONENT", "HA", "SEASON_LEVEL", "DATA", "Squadra", "Bench Points", "Starter Points"]
exclude_stats_ha_2 = ['No', 'Player', 'MIN',  'FG%', '3P%',  '2P%', 'FT%',  'PIR', 'EFF','+/-', 'OPPONENT', 'WL', 'SEASON_LEVEL', 'DATA']
exclude_stats_wl_2 = ['No', 'Player', 'MIN',  'FG%', '3P%',  '2P%', 'FT%',  'PIR', 'EFF','+/-', 'OPPONENT', 'HA', 'SEASON_LEVEL', 'DATA']

# --- HA Table 1 ---
df_match_opponents_melt_ha = df_match_opponents.melt(id_vars='HA', var_name='Statistica', value_name='Valore')
# grouping the melted df by HA and Statistica and summing Valore where the statistica is not Best Partial,OPPONENT,WL,SEASON_LEVEL,DATA
df_match_opponents_grouped_ha = (
    df_match_opponents_melt_ha
    .loc[~df_match_opponents_melt_ha["Statistica"].isin(exclude_stats_ha)]
    .groupby(["HA", "Statistica"], as_index=False)["Valore"]
    .mean()
    .round(2)
)
df_match_opponents_pivot_ha = df_match_opponents_grouped_ha.pivot(index='Statistica', columns='HA', values='Valore').reset_index()
print("Pivot HA:", df_match_opponents_pivot_ha.shape)

# --- WL Table 1 ---
df_match_opponents_melt_wl = df_match_opponents.melt(id_vars='WL', var_name='Statistica', value_name='Valore')
# grouping the melted df by HA and Statistica and summing Valore where the statistica is not Best Partial,OPPONENT,WL,SEASON_LEVEL,DATA
df_match_opponents_grouped_wl = (
    df_match_opponents_melt_wl
    .loc[~df_match_opponents_melt_wl["Statistica"].isin(exclude_stats_wl)]
    .groupby(["WL", "Statistica"], as_index=False)["Valore"]
    .mean()
    .round(2)
)
df_match_opponents_pivot_wl = df_match_opponents_grouped_wl.pivot(index='Statistica', columns='WL', values='Valore').reset_index()
print("Pivot WL:", df_match_opponents_pivot_wl.shape)

# --- HA Table 2 ---
df_opponents_melt_ha = df_opponents.melt(id_vars='HA', var_name='Statistica', value_name='Valore')

df_opponents_grouped_ha = (
    df_opponents_melt_ha
    .loc[~df_opponents_melt_ha["Statistica"].isin(exclude_stats_ha_2)]
    .groupby(["HA", "Statistica"], as_index=False)["Valore"]
    .mean()
    .round(2)
)

# --- Calcolo percentuali 2P% e 3P% ---
# Trasformiamo in wide format per accedere facilmente ai valori
df_wide_ha = df_opponents_grouped_ha.pivot(index="HA", columns="Statistica", values="Valore")
# Calcolo percentuali (evita divisione per 0)
df_wide_ha["2P%"] = np.where(df_wide_ha["2PA"] > 0, df_wide_ha["2PM"] / df_wide_ha["2PA"] * 100, np.nan)
df_wide_ha["3P%"] = np.where(df_wide_ha["3PA"] > 0, df_wide_ha["3PM"] / df_wide_ha["3PA"] * 100, np.nan)
df_wide_ha["FT%"] = np.where(df_wide_ha["FTA"] > 0, df_wide_ha["FTM"] / df_wide_ha["FTA"] * 100, np.nan)

# Arrotondiamo
df_wide_ha[["2P%", "3P%", "FT%"]] = df_wide_ha[["2P%", "3P%", "FT%"]].round(2)

# Torniamo in formato lungo per aggiungerle al grouped
df_percentuali_ha = df_wide_ha[["2P%", "3P%", "FT%"]].reset_index().melt(
    id_vars="HA",
    var_name="Statistica",
    value_name="Valore"
)

# --- Combiniamo ---
df_opponents_grouped_ha = pd.concat([df_opponents_grouped_ha, df_percentuali_ha], ignore_index=True)

# --- Pivot finale (se ti serve per la visualizzazione)
df_opponents_pivot_ha = df_opponents_grouped_ha.pivot(index='Statistica', columns='HA', values='Valore').reset_index()

print("Pivot HA:", df_opponents_pivot_ha.shape)


# --- WL Table 2 ---
df_opponents_melt_wl = df_opponents.melt(id_vars='WL', var_name='Statistica', value_name='Valore')
df_opponents_grouped_wl = (
    df_opponents_melt_wl
    .loc[~df_opponents_melt_wl["Statistica"].isin(exclude_stats_wl_2)]
    .groupby(["WL", "Statistica"], as_index=False)["Valore"]
    .mean()
    .round(2)
)

# --- Calcolo percentuali 2P% e 3P% ---
# Trasformiamo in wide format per accedere facilmente ai valori
df_wide_wl = df_opponents_grouped_wl.pivot(index="WL", columns="Statistica", values="Valore")
# Calcolo percentuali (evita divisione per 0)
df_wide_wl["2P%"] = np.where(df_wide_wl["2PA"] > 0, df_wide_wl["2PM"] / df_wide_wl["2PA"] * 100, np.nan)
df_wide_wl["3P%"] = np.where(df_wide_wl["3PA"] > 0, df_wide_wl["3PM"] / df_wide_wl["3PA"] * 100, np.nan)
df_wide_wl["FT%"] = np.where(df_wide_wl["FTA"] > 0, df_wide_wl["FTM"] / df_wide_wl["FTA"] * 100, np.nan)

# Arrotondiamo
df_wide_wl[["2P%", "3P%", "FT%"]] = df_wide_wl[["2P%", "3P%", "FT%"]].round(2)

# Torniamo in formato lungo per aggiungerle al grouped
df_percentuali_wl = df_wide_wl[["2P%", "3P%", "FT%"]].reset_index().melt(
    id_vars="WL",
    var_name="Statistica",
    value_name="Valore"
)

# --- Combiniamo ---
df_opponents_grouped_wl = pd.concat([df_opponents_grouped_wl, df_percentuali_wl], ignore_index=True)

# --- Pivot finale (se ti serve per la visualizzazione)
df_opponents_pivot_wl = df_opponents_grouped_wl.pivot(index='Statistica', columns='WL', values='Valore').reset_index()

print("Pivot HA:", df_opponents_pivot_wl.shape)

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

    '''# --- HA Table 1 ---
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
    '''

    # --- Filter for graph ---
    df_filtered = df_opponents_merged[
        df_opponents_merged['HA_match'].isin(home_away) &
        df_opponents_merged['WL_match'].isin(win_lose)
    ]
    print("Filtered rows:", len(df_filtered))
    print("Columns:", df_filtered.columns.tolist()[:10])

    # --- Build DataTable data ---
    data_ha = df_match_opponents_pivot_ha.to_dict('records')
    columns_ha = [{"name": i, "id": i, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)} 
                  for i in df_match_opponents_pivot_ha.columns]
    data_wl = df_match_opponents_pivot_wl.to_dict('records')
    columns_wl = [{"name": i, "id": i, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)} 
                  for i in df_match_opponents_pivot_wl.columns]

    data_ha_2 = df_opponents_pivot_ha.to_dict('records')
    columns_ha_2 = [{"name": i, "id": i, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)} 
                    for i in df_opponents_pivot_ha.columns]
    data_wl_2 = df_opponents_pivot_wl.to_dict('records')
    columns_wl_2 = [{"name": i, "id": i, "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)} 
                    for i in df_opponents_pivot_wl.columns]



    # --- Graph ---
if df_filtered.empty:
    fig = go.Figure()
    fig.update_layout(
        title="⚠️ Nessun dato disponibile per i filtri selezionati",
        height=400,
        autosize=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
else:
    if statistica not in df_filtered.columns:
        if f"{statistica}_match" in df_filtered.columns:
            statistica = f"{statistica}_match"

    # ✅ Ricrea figura da zero (non cumulativa)
    fig = go.Figure()

    # Aggiungi le barre manualmente — evita duplicazioni di px.bar()
    for wl in df_filtered["WL_match"].unique():
        for ha in df_filtered["HA_match"].unique():
            subset = df_filtered[(df_filtered["WL_match"] == wl) & (df_filtered["HA_match"] == ha)]
            fig.add_trace(go.Bar(
                x=subset["OPPONENT"],
                y=subset[statistica],
                name=f"{wl} ({ha})",
                marker=dict(
                    color="green" if wl == "W" else "red",
                    line=dict(width=1, color="black")
                ),
                opacity=0.85
            ))

    # Layout pulito, fisso e coerente
    fig.update_layout(
        title=f"{statistica} per avversario",
        barmode="group",
        height=450,              # dimensione fissa
        autosize=False,          # 🔥 evita crescita
        margin=dict(t=60, b=60, l=60, r=60),
        plot_bgcolor="rgba(245,245,245,1)",
        paper_bgcolor="white",
        transition=dict(duration=0),  # disabilita animazioni
        xaxis=dict(fixedrange=True),  # evita zoom/rescale automatico
        yaxis=dict(fixedrange=True)
    )

print("=== Callback completed ===")
return data_ha, columns_ha, data_wl, columns_wl, fig, data_ha_2, columns_ha_2, data_wl_2, columns_wl_2


