import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# deciding the order of the pages in the sidebar
page_order = ['/', '/page-1', '/page-2', '/page-3']#, '/page-4', '/page-5']

# starting the dash application
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

# setting the sidebar
sidebar = html.Div(
    [
#        html.H3("Our Offers", className="display-4"),
        html.Hr(),
        html.P("Choose one page", className="lead"
        ),
        dbc.Nav(
            [ # connecting the app.py file to all the other files
              # that we want in the sidebar
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Statistiche per partita", href="/page-1", active="exact"),
                dbc.NavLink("Statistiche di tiro", href="/page-2", active="exact"),
                dbc.NavLink("Pagina Difesa", href="/page-3", active="exact")
                #dbc.NavLink("Trap and Spell Cards", href="/page-4", active="exact"),
                #dbc.NavLink("End Page", href="/page-5", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
)

# setting the layout
app.layout = dbc.Container([
    # dbc.Row([
    #     dbc.Col(html.Div("Data Driven Yu-Gi-Oh Deck Building ",
    #                      style={'fontSize':50, 'textAlign':'center'}))
    # ]),

    # html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)

# letting the app run
if __name__ == "__main__":
    app.run(debug=False)
    
    
    
