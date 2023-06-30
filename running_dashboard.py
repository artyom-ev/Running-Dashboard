import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Data 
data = pd.read_csv('running_data.csv', parse_dates = ['WorkoutDay'])

# Functions to be used in Dashboard
def make_break(num_breaks):
    '''Creates given number of breaks'''
    br_list = [html.Br()] * num_breaks
    return br_list

# Plots to be used in Dashboard
hr_hist = px.histogram(data,
                  x='HeartRateAverage',
                  nbins=40,
                  color_discrete_sequence=["rgb(102, 103, 171)"],
                  opacity=0.8)

# Some stuff to be used in Dashboard
types = data['Title'].unique()

# Defining table
data_cols = [x for x in data.columns]
d_columns = [{'name': x, 'id': x} for x in data_cols]
d_table = dash_table.DataTable(
            columns=d_columns,
            data=data.to_dict('records'),
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_current=0,
            page_size=10,
  			# Align all cell contents left
  			style_cell=({'textAlign':'left'}),
  			# Style the background of money columns
  			style_cell_conditional=[],
 			# Style all headers
  			style_header={'background-color':'rgb(168, 255, 245)'}
  			)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Running Performance Dashboard'),
    html.Div(
        children=[
        html.Div(
            children=[
            html.H2('Controls'),
            html.Br(),
            html.H3('Workout type select'),
            dcc.Dropdown(id='workout_type_dd',
                        options=[
                            {'label':'Base', 'value':'Base'},
                            {'label':'Fartlek', 'value':'Fartlek'},
                            {'label':'Tempo', 'value':'Tempo'},
                            {'label':'Progression', 'value':'Progression'},
                            {'label':'Intervals', 'value':'Intervals'}],
                            style={'width':'200px', 'margin':'0 auto'})
                    ],
            style={'width':'350px', 'height':'350px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}
                ),
        html.Div(
            children=[
                dcc.Graph(id='hr_pace'),
                
                    ],
            style={'width':'700px','display':'inline-block'}
                ),
                    ]),
    html.Div(
        children=[
        html.H2('Training Calendar'),
        dcc.Dropdown(id='type-filter',
                    options=[{'label': type, 'value': type} for type in types],
                    value=types,
                    multi=True
                    ),
        dcc.Graph(
                id='hr_scatter',
                figure={}
                )]
            ),
    *make_break(5),
    html.H2('Heart Rate Info'),
    html.Div(
        children=[
        html.Span(children=[
                'Maximum and Minimum values of heart rate:',
                html.Ul(children=[
                html.Li(children=['Min value: ', data['HeartRateAverage'].min()]),
                html.Li(children=['Max value: ', data['HeartRateAverage'].max()])
                                ]),
                            ],style={'display':'inline-block', 'vertical-align':'top'}),
        dcc.Graph(
                id='hr_hist',
                figure=hr_hist,
                style={'display':'inline-block'}
                )
                ]
            ),
    html.Div(
        children=[
        html.H2('Data Table Preview'),
        d_table
                ],
        style={'width':'850px', 'height':'750px', 'margin':'0 auto'}
            )
    ],                  
    style={'text-align':'center', 'width':'100%'}
)

@app.callback(
    Output(component_id='hr_pace', component_property='figure'),
    Input(component_id='workout_type_dd', component_property='value'))

def update_plot(input_type):
    type_filter = 'All Types'
    run = data.copy(deep=True)
    if input_type:
        type_filter = input_type
        run = run[run['Title'] == type_filter]
    run_scatter = px.scatter(
        title=f'Running type is {type_filter}', data_frame=run, x='Pace', y='HeartRateAverage', color='Title')
    return run_scatter

@app.callback(
    Output(component_id='hr_scatter', component_property='figure'),
    Input(component_id='type-filter', component_property='value'))

def update_scatter(types_selected):
    filtered_data = data[data['Title'].isin(types_selected)]
    scatter_fig = px.scatter(
                        filtered_data,
                        x = 'WorkoutDay',
                        y = 'HeartRateAverage',
                        color='Title')
    return scatter_fig




if __name__ == '__main__':
    app.run_server(debug=True)
    
    

