import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# ✅ registra la pagina (obbligatorio per multipage)
dash.register_page(__name__, path='/page-2', name='Statistiche tiro giocatore')

# === Dataset ===
df_luiss_giocatori = pd.read_csv(
    "/Users/leo/Desktop/me 2/Scouting/Scouting_2025-2026/Test/tables/df_players_luiss.csv",
    sep=';'
)

# === Componenti ===
giocatori = dcc.Dropdown(
    id='giocatori',
    options=[{'label': i, 'value': i} for i in df_luiss_giocatori['Player'].unique()],
    value=[df_luiss_giocatori['Player'].iloc[0]],
    multi=True,
    clearable=False
)

home_away = dcc.Checklist(
    id='ha',
    options=[
        {'label': 'Casa', 'value': 'H'},
        {'label': 'Trasferta', 'value': 'A'}
    ],
    value=['H'],
    labelStyle={'display': 'block'}
)

win_lose = dcc.Checklist(
    id='wl',
    options=[
        {'label': 'W', 'value': 'W'},
        {'label': 'L', 'value': 'L'}
    ],
    value=['W'],
    labelStyle={'display': 'block'}
)

# === Layout ===
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Analisi Per Giocatore'),
            html.P("In questa sezione è possibile vedere le statistiche di tiro "
                   "filtrate per giocatore, vittoria/sconfitta e casa/trasferta.")
        ]), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Casa/Trasferta'),
            home_away,
            html.Br(),
            html.Label('W/L'),
            win_lose,
            html.Br(),
            html.Label('Giocatori'),
            giocatori
        ], width=3, style={'padding': '20px'}),

        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='radar1'), width=6),
                dbc.Col(dcc.Graph(id='radar2'), width=6)
            ])
        ], width=9)
    ])
], fluid=True)

# === Callback ===
@callback(
    Output('radar1', 'figure'),
    Output('radar2', 'figure'),
    Input('giocatori', 'value'),
    Input('ha', 'value'),
    Input('wl', 'value')
)
def update_radar(giocatori_sel, ha_sel, wl_sel):

    campi_gruppo1 = ['2PA_tot', '2PM_tot', '3PM_tot', '3PA_tot', 'FTM_tot', 'FTA_tot']
    campi_gruppo2 = ['2P%_tot', '3P%_tot', 'FT%_tot']

    dff = df_luiss_giocatori[
        (df_luiss_giocatori['Player'].isin(giocatori_sel)) &
        (df_luiss_giocatori['HA'].isin(ha_sel)) &
        (df_luiss_giocatori['WL'].isin(wl_sel))
    ]

    dff_filtered = dff.copy()
    dff_filtered['2PA_tot'] = dff.groupby(['Player', 'HA', 'WL'])['2PA'].transform('sum')
    dff_filtered['2PM_tot'] = dff.groupby(['Player', 'HA', 'WL'])['2PM'].transform('sum')
    dff_filtered['3PA_tot'] = dff.groupby(['Player', 'HA', 'WL'])['3PA'].transform('sum')
    dff_filtered['3PM_tot'] = dff.groupby(['Player', 'HA', 'WL'])['3PM'].transform('sum')
    dff_filtered['FTA_tot'] = dff.groupby(['Player', 'HA', 'WL'])['FTA'].transform('sum')
    dff_filtered['FTM_tot'] = dff.groupby(['Player', 'HA', 'WL'])['FTM'].transform('sum')
    dff_filtered['2P%_tot'] = dff_filtered.apply(lambda row: (row['2PM_tot'] / row['2PA_tot'] * 100) if row['2PA_tot'] > 0 else 0, axis=1)
    dff_filtered['3P%_tot'] = dff_filtered.apply(lambda row: (row['3PM_tot'] / row['3PA_tot'] * 100) if row['3PA_tot'] > 0 else 0, axis=1)
    dff_filtered['FT%_tot'] = dff_filtered.apply(lambda row: (row['FTM_tot'] / row['FTA_tot'] * 100) if row['FTA_tot'] > 0 else 0, axis=1)

    fig1, fig2 = go.Figure(), go.Figure()

    for player in giocatori_sel:
        df_player = dff_filtered[dff_filtered['Player'] == player]
        if df_player.empty:
            continue

        values1 = [df_player[campi_gruppo1].mean()[c] for c in campi_gruppo1]
        values2 = [df_player[campi_gruppo2].mean()[c] for c in campi_gruppo2]

        fig1.add_trace(go.Scatterpolar(
            r=values1 + [values1[0]],
            theta=campi_gruppo1 + [campi_gruppo1[0]],
            fill='toself',
            name=player
        ))

        fig2.add_trace(go.Scatterpolar(
            r=values2 + [values2[0]],
            theta=campi_gruppo2 + [campi_gruppo2[0]],
            fill='toself',
            name=player
        ))

    for f in [fig1, fig2]:
        f.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            template='plotly_white'
        )

    fig1.update_layout(title="Radar Plot – Volumi di tiro (2P, 3P, FT)")
    fig2.update_layout(title="Radar Plot – Percentuali di realizzazione")

    return fig1, fig2
