#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:28:09 2023

@author: leo
"""

import dash
from dash import html
import dash_bootstrap_components as dbc
from pathlib import Path
import base64

dash.register_page(__name__, path='/', name='Home')

# === costruisco il path reale del file immagine ===
# cartella dove sta QUESTO file (es. .../pages)
current_dir = Path(__file__).resolve().parent

# cartella padre (es. .../ , la root del progetto)
parent_dir = current_dir.parent

# cartella data nella root
data_dir = parent_dir / "data"

#data_dir = parent_dir

# file immagine dentro data
image_file = data_dir / "logo_luiss.jpg"

# leggo e converto in base64
encoded_image = base64.b64encode(open(image_file, "rb").read()).decode()

# costruisco la stringa da dare a <img src="...">
image_src = f"data:image/jpeg;base64,{encoded_image}"
# se il logo è png cambia in image/png

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '25px'})
        ])
    ], justify='center'),

    # BLOCCO INTRO CON IMMAGINE + TESTO
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(style={'height': '50px'})
            ])
        ], justify='center'),

        # IMMAGINE
        html.Div(
            html.Img(
                src=image_src,           # <-- ora è una data URI, niente URL esterno
                style={
                    'width': '400px',
                    'height': 'auto',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                }
            )
        ),

        # TESTO
        html.P(
                """Hi, and welcome to this basketball stats analysis page!!!
            Here you will be able to find some stats of the Luiss Serie D team, attending the DR! Championship; the analysis is based on performances
            of the team both offensively and defensively. There will be sections showing stats by player and sections showing stats by team.
            Any recommendations on analyses to show will be very appreciated.
            Do not hesitate to contact me.""",
                style={'whiteSpace': 'pre-wrap'}
            )
    ]),

    html.Div([
        html.H3('Our Data'),
        html.P(
                """Our data is recorded using the Basketball Stats Assistant app during each match of the championship.
            During each game someone on the team (mostly the TM) takes stats about LUISS players, LUISS team and the opponent team;
            they are then uploaded into specific tables through a data engineering Python process and shown in dashboards using Dash.""",
                style={'whiteSpace': 'pre-wrap'}
            )
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '50px'})
        ])
    ], justify='center')
])
