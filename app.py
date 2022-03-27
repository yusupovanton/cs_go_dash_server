from handlers.dispatcher import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


def db_to_df():

    list_of_rows = []

    for key in r.keys():
        list_of_rows.append(r.hgetall(key))

    df = pd.DataFrame(list_of_rows)

    df['float'] = df['float'].str.strip()
    df['float'] = df['float'].astype(str).replace(' ', '')
    df['float'] = df['float'].astype(float)
    df['price'] = df['price'].str.replace(' ', '')
    df['price'] = df['price'].astype(float)
    df['id'] = df['id'].astype(int)

    return df


df = db_to_df()

duplicates_series = df.pivot_table(columns=['name'], aggfunc='size')
duplicates_df = pd.DataFrame({'name': duplicates_series.index, 'count': duplicates_series.values})
duplicates_fig = px.bar(duplicates_df, x='name', y='count')

app.layout = html.Div([

    html.H4('Price of cs:go skins'),
    html.H5(f'The current amount of unique skins in the database is: {len(r.keys())}'),
    dcc.Graph(id="Graph"),
    dcc.Dropdown(id='Dropdown', options=[{'label': i, 'value': i} for i in df.name.unique()]),
    dcc.Graph(figure=duplicates_fig, id='Total Skins'),

    dcc.Interval(
            id='interval-component',
            interval=10*1000,  # in milliseconds
            n_intervals=0
        )
])


@app.callback(
    Output('Graph', 'figure'),
    Input('Dropdown', 'value'))
def update_output(selected_value):

    filtered_df = df[df['name'] == selected_value]
    fig = px.scatter(filtered_df, x="float", y="price", hover_name="name", hover_data=["id", "exterior", "price"],
                     trendline="lowess")
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.update_layout(transition_duration=500)

    return fig


@app.callback(Output('Total Skins', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df = db_to_df()
    duplicates_series = df.pivot_table(columns=['name'], aggfunc='size')
    duplicates_df = pd.DataFrame({'name': duplicates_series.index, 'count': duplicates_series.values})
    fig = px.bar(duplicates_df, x='name', y='count')

    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
