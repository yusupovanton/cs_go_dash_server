from handlers.dispatcher import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = db_to_df()


'''GRAPHS AND FIGURES'''

# main figure and expensiveness coefficient
df['expensiveness_coefficient'] = df.price * df.float
main_fig = px.scatter(df,
                      x='float',
                      y='price',
                      title="Price of chosen skins by float",
                      color='expensiveness_coefficient')

# expensiveness figure and df column
df_exp = df.pivot_table(index="id", values=["name", "expensiveness_coefficient", "price"], aggfunc=np.min)
df_exp = df_exp.sort_values(by="expensiveness_coefficient", ascending=False)
df_exp = df_exp.head(50)
expensiveness_fig = px.bar(df_exp,
                           x='name',
                           y='expensiveness_coefficient',
                           title='50 most expensive skins based on price and float',
                           color='price',
                           color_continuous_scale='aggrnyl')
expensiveness_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# amount graph
duplicates_series = df.pivot_table(columns=['name'], aggfunc='size')
duplicates_df = pd.DataFrame({'name': duplicates_series.index, 'count': duplicates_series.values})
duplicates_df = duplicates_df.sort_values(by="count", ascending=False)
duplicates_df = duplicates_df.head(50)
duplicates_fig = px.bar(duplicates_df, color='count', x='name', y='count',
                        title='Count of various skins in the base', color_continuous_scale='aggrnyl')
duplicates_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

'''LAYOUT'''
header = html.Div([
    html.H4(f"Price of cs:go skins", style=styles['H4']),
    html.H5(f"Current number of skins in the db is {len(r.keys())}")], style=styles['H5']
)

dropdowns = html.Div([
        dcc.Dropdown(
                        id="N_Dropdown",
                        options=[{'label': i, 'value': i} for i in df['name'].unique()],
                        value=None,
                        placeholder="Name"),

        dcc.Dropdown(
                        id="E_Dropdown",
                        options=[{'label': i, 'value': i} for i in df['exterior'].unique()],
                        value=None,
                        placeholder="Exterior")
], style=styles['DIV'])

body = html.Div([
    dcc.Graph(figure=duplicates_fig, id='Total Skins'),
    dcc.Graph(figure=expensiveness_fig, id='Cheapest Skins'),
    dcc.Graph(figure=main_fig, id='Main Graph'),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                    **Hover Data**

                    Point mouse over values in the graph to get skin properties.
                    
                """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),
        html.Div([
            dcc.Markdown("""
                **Link**

                Click on points on the graph to get a buy link to it.
            """),
            html.Pre(id='click-data1', style=styles['pre']),
        ], className='three columns'),
        html.Div([
            dcc.Markdown("""
                **Skin Image**

                Click on points on the graph to get an image of this weapon skin.
            """),
            html.Pre(id='click-data2', style=styles['pre']),
        ], className='three columns')])

])

footer = html.Div([
    dcc.Interval(
                id='interval-component',
                interval=3600*1000,  # in milliseconds
                n_intervals=0)
])

app.layout = html.Div([
    header, dropdowns, body, footer
])


'''PAGE UPDATES, INPUTS, CALLBACKS'''


@app.callback(
    Output('Main Graph', 'figure'),
    Input('N_Dropdown', 'value'),
    Input('E_Dropdown', 'value')
)
def update_output(selected_name, selected_ext):

    filters = {
        'name': selected_name,
        'exterior': selected_ext
    }

    filtered_df = filter_df(filters=filters, df=df)

    fig = px.scatter(filtered_df,
                     x="float",
                     y="price",
                     hover_name="name",
                     hover_data=["id", "exterior", "price", "expensiveness_coefficient", "link", "img",
                                 "stickers"],
                     trendline="ols",
                     color='expensiveness_coefficient',
                     color_continuous_scale='aggrnyl',
                     trendline_color_override="yellow")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


@app.callback(Output('Total Skins', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df = db_to_df()

    duplicates_series = df.pivot_table(columns=['name'], aggfunc='size')
    duplicates_df = pd.DataFrame({'name': duplicates_series.index, 'count': duplicates_series.values})
    duplicates_df = duplicates_df.sort_values(by="count", ascending=False)
    duplicates_df = duplicates_df.head(50)

    fig = px.bar(duplicates_df, color='count', x='name', y='count',
                 title='Count of various skins in the base', color_continuous_scale='aggrnyl')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


@app.callback(
    Output('hover-data', 'children'),
    Input('Main Graph', 'hoverData'))
def display_hover_data(hoverData):

    if hoverData and hoverData['points'][0]['curveNumber'] == 0:
        stickers = 'None'
        if str(hoverData['points'][0]['customdata'][5]) == 'None':
            stickers = 'None'
        else:
            stickers = hoverData['points'][0]['customdata'][5].split('\n')
            stickers = [x.split('title="')[1].split('"')[0] for x in stickers]

        return json.dumps({'Float:': hoverData['points'][0]['x'],
                           'Price:': hoverData['points'][0]['y'],
                           'Expensiveness': hoverData['points'][0]['customdata'][2],
                           'Stickers': str(stickers)}, indent=2)


@app.callback(
    Output('click-data1', 'children'),
    Input('Main Graph', 'clickData'))
def display_click_data(clickData):
    if clickData:
        return html.A(clickData['points'][0]['customdata'][3])


@app.callback(
    Output('click-data2', 'children'),
    Input('Main Graph', 'clickData'))
def display_click_data(clickData):
    if clickData:
        return html.Img(src=clickData['points'][0]['customdata'][4])


if __name__ == '__main__':
    app.run_server(debug=True)
