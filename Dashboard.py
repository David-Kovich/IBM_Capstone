# IBM Capstone SpaceX Plotly/Dash Lab
# David Kovich

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

spacex_df = pd.read_csv('IBM Data Science\spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
        options=[{'label':'All Sites', 'value':'ALL'},
            {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
            {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
            {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
            {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}],
        value='ALL',
        placeholder='Select Launch Site',
        searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,marks={0:'0',10000:'10000'},value=[min_payload,max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
    ])

# TASK 2:   Add a callback function for `site-dropdown` as input, 'success-pie-chart' as output
#   the return value of 'get_pie_chart', i.e. 'fig', will map to the component 'success-pie-chart'
#   the input value to 'get_pie_chart', i.e. 'entered_site', will map to the value selected in the 'site-dropdown' menu
#               
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success Chart')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        vals = [filtered_df['class'].sum(), len(filtered_df.index) - filtered_df['class'].sum()]
        fig = px.pie(filtered_df, values=vals, names=['Success', 'Failure'], title='Success Chart')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')])
def get_scatter_chart(site,payload):
    if site == 'ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] > payload[0]]
        filtered_df2 = filtered_df[filtered_df['Payload Mass (kg)'] < payload[1]]
        fig = px.scatter(filtered_df2,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        filtered_df2 = filtered_df[filtered_df['Payload Mass (kg)'] > payload[0]]
        filtered_df3 = filtered_df2[filtered_df2['Payload Mass (kg)'] < payload[1]]
        fig = px.scatter(filtered_df3,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()