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
            'Hi, we are three students attending the Data Visualization course, '
            'we are old fans of the yu-gi-oh game. With this web site we would '
            'like to help new players that like this game (as we did) to build the deck they '
            'most preferred based on the data we have gathered. What the user of '
            'this page will find will be some static graphs showing the type of data '
            'that have been used and then some interactive graphs that will be useful '
            'in the construction of the deck.'
        )
    ]),

    html.Div([
        html.H3('Our Data'),
        html.P(
            'In order to build this web site we retrieved our data from an '
            'API about Yu-Gi-Oh cards. Inside that dataset there were quite '
            'a lot of data and after having cleaned them a bit we decided to '
            'construct a dataset with the most useful data to solve '
            'our task. Therefore, the data we will be using all along the '
            'journey in the site are data about the card name, their type, '
            'the attribute of the monster cards, their attack, defense and '
            'level, the price of the cards and the names of the sets in '
            'which they are used and the rarity of the sets.'
        )
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '50px'})
        ])
    ], justify='center')
])
