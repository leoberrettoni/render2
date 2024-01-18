import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Read the CSV file
df = pd.read_csv('Mappa_di_tiro.csv', sep=',')

# Function to draw a basketball court on the plotly figure
def draw_court_plotly(fig, color='black', lw=2):
    # Basketball hoop, Backboard, Outer box of the paint, etc.
    # Add shapes to represent the basketball court

    # Basketball hoop
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=5 - 0.75, y0=25 - 0.75, x1=5 + 0.75, y1=25 + 0.75,
                  line=dict(color=color, width=lw))

    # Backboard
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=4, y0=22, x1=3.5, y1=28,
                  line=dict(color=color, width=lw))

    # Outer box of the paint
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=0, y0=17, x1=19, y1=33,
                  line=dict(color=color, width=lw))

    # Free throw top arc
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=19 - 6, y0=25 - 6, x1=19 + 6, y1=25 + 6,
                  line=dict(color=color, width=lw))

    # 3pt line - arcs
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=5 - 23.75, y0=25 - 23.75, x1=5 + 23.75, y1=25 + 23.75,
                  line=dict(color=color, width=lw))

    # 3pt line - side lines
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=-1, y0=3, x1=-1, y1=17,
                  line=dict(color=color, width=lw))
    fig.add_shape(type="rect",
                  xref="x", yref="y",
                  x0=-1, y0=33, x1=-1, y1=47,
                  line=dict(color=color, width=lw))

    # Remove axis labels and set range
    fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 50]),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 50]),
                      plot_bgcolor='white', 
                      margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor='white',
                      height=450)

    return fig

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

# Define components for the app layout
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(id='basketball-court-graph')

# Define dropdown menus for players and matches
dropdown1 = dcc.Dropdown(
    id='player-dropdown',
    options=[{'label': i, 'value': i} for i in df['Giocatore'].unique()],
    value=['Alessio', 'Fala'],
    multi=True,
    clearable=False
)

dropdown2 = dcc.Dropdown(
    id='match-dropdown',
    options=[{'label': i, 'value': i} for i in df['Partita'].unique()],
    value=['San Cesareo'],
    multi=True,
    clearable=False
)

# Define the layout of the app
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2('Mappa di tiro'),
            html.Div([
                html.P("In questa sezione è possibile visualizzare varie mappe di tiro. È possibile\
                filtrare per giocatore o per partita a seconda delle informazioni che si vogliono ottenere.")
                ])
        ]))]),
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([html.Label('Giocatori'), dropdown1], width=6),
        dbc.Col([html.Label('Partita'), dropdown2], width=6)
    ], justify='left'),
    dbc.Row([
        dbc.Col([
            html.Div(style={'height': '100px'})
            ])
        ], justify='center')
], fluid=True)

# Define callback for updating the graph
@app.callback(
    Output('basketball-court-graph', 'figure'),
    [Input('player-dropdown', 'value'), Input('match-dropdown', 'value')]
)
def update_graph(giocatore, partita):
    # Filter the dataframe according to user input
    filtered_df = df[(df['Giocatore'].isin(giocatore)) & (df['Partita'].isin(partita))]

    # Define the scatter plot for shots
    made_shots = filtered_df[filtered_df['made'] == 1]
    missed_shots = filtered_df[filtered_df['made'] == 0]

    # Create a figure and add court layout
    fig = go.Figure()
    draw_court_plotly(fig)

    # Add made and missed shots as scatter points
    fig.add_trace(go.Scatter(x=made_shots['x'], y=made_shots['y'],
                             mode='markers', name='Made',
                             marker=dict(color='green', size=10, line=dict(color='black', width=1)),
                             text=made_shots['Giocatore'].astype(str) + ' - ' + made_shots['Partita'].astype(str),
                             hoverinfo='text'))
    fig.add_trace(go.Scatter(x=missed_shots['x'], y=missed_shots['y'],
                             mode='markers', name='Missed',
                             marker=dict(color='red', size=10, symbol='x'),
                             text=missed_shots['Giocatore'].astype(str) + ' - ' + missed_shots['Partita'].astype(str),
                             hoverinfo='text'))
    
    # Update layout
    fig.update_layout(showlegend=True, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), width=800, height=600)

    return fig

# Set the layout and run the server
if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug
