from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output

app = Dash(__name__)

df = pd.read_csv('master.csv')

dff = df.copy()
gb_country = dff.groupby('country').sum()
sr_country = ((gb_country['suicides_no'] / gb_country['population']) * (10**5)).reset_index()
sr_country.columns=['Country Name', 'Suicide Rate (per 100K)']

fig = px.choropleth(
    data_frame = sr_country,
    locationmode = 'country names',
    locations = 'Country Name',
    scope='world',
    color= 'Suicide Rate (per 100K)',
    #hover_data=sr_country,
    hover_name = 'Country Name',
    color_continuous_scale=px.colors.sequential.Viridis,
    template = 'ggplot2'
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(visible=False, showcountries=True)

# -------------------------------------------------------------------------------------------------------------------
# Layout

app.layout = html.Div(children=[
    html.H1(children='Suicide Data Dashboard', style={'text-align':'center'}),

    html.Div(children='''
            Suicide rate across countries per 100K Population from 1985-2016
            ''',
            style={'text-align':'center'}),

    dcc.Graph(
        id='suicide-map',
        figure=fig
    )
])

# -------------------------------------------------------------------------------------------------------------------
# Callbacks
"""
@app.callback(
    Output(component_id='suicide-map', component_property='figure')
)

def create_graphs():

    dff = df.copy()
    gb_country = dff.groupby('country').sum()
    sr_country = ((gb_country['suicides_no'] / gb_country['population']) * (10**5))

    fig = px.chloropleth(
    data_frame = sr_country,
    locationmode = 'country_names',
    locations = sr_country.index,
    scope='world',
    color= sr_country,
    hover_data=sr_country,
    color_continuous_scale=px.colors.sequential.Viridis

    )

    return fig
"""    


if __name__ == '__main__':
    app.run_server(debug=True)