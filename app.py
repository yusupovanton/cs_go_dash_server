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
    dcc.Graph(id="Graph"),
    dcc.Dropdown(id='Dropdown', options=[{'label': i, 'value': i} for i in df.name.unique()]),
    dcc.Graph(figure=duplicates_fig, id='Total Skins')
])


@app.callback(
    Output('Graph', 'figure'),
    Input('Dropdown', 'value'))
def update_output(selected_value):

    filtered_df = df[df['name'] == selected_value]
    fig = px.scatter(filtered_df, x="float", y="price", hover_name="name", hover_data=["id", "exterior", "price"])

    fig.update_layout( transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
