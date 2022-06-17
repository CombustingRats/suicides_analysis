from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output

app = Dash(__name__)

df = pd.read_csv('master.csv')

# -------------------------------------------------------------------------------------------------------------------
# Data Processing

dff = df.copy()

dff.drop(labels=['HDI for year', 'country-year'], axis=1, inplace=True)
gb_country = dff.groupby('country').sum()
sr_country = ((gb_country['suicides_no'] / gb_country['population']) * (10**5)).reset_index()
sr_country.columns=['Country Name', 'Suicide Rate (per 100K)']

# -------------------------------------------------------------------------------------------------------------------
# Figure Generation

fig = px.choropleth(
    data_frame = sr_country,
    locationmode = 'country names',
    locations = 'Country Name',
    scope='world',
    color= 'Suicide Rate (per 100K)',
    #hover_data=sr_country,
    hover_name = 'Country Name',
    color_continuous_scale=px.colors.sequential.Viridis,
    template = 'ggplot2',
    title='Suicide Rate Across Countries',
    height=350
)
fig.update_layout(title_text = 'Suicide Rate Across Countries')
fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'} ,margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(visible=False, showcountries=True)

gb_year = df.groupby('year').sum()
suicide_rate = (gb_year['suicides_no'] / gb_year['population'] * (10**5)).reset_index()
suicide_rate.columns = ['Year','Suicide Rate (per 100k)']
fig2 = px.line(suicide_rate, 
            x="Year", 
            y="Suicide Rate (per 100k)", 
            title="Yearly Suicide Rates",
            template='ggplot2',
            markers=True,
            height=400)
fig2.update_layout(title_text='By Year of Occurance', 
            title_font_family="Courier", 
            title_x=0.1)
fig2.add_annotation(x=1995, 
                    y=15.3,
                    text='Suicide Rates Peaked in 1995',
                    showarrow=True,
                    arrowhead=1
                    )
fig2.add_annotation(x=2015, 
                    y=11.47,
                    text='Suicide Rates Reached a Minimum in 2015',
                    showarrow=True,
                    arrowhead=1,
                    ax=10,
                    ay=20
                    )

gb_sex = df.groupby('sex').sum()
sr_sex = ((gb_sex['suicides_no'] / gb_sex['population']) * (10 ** 5)).reset_index()
sr_sex.columns = ['Sex','Suicide Rate (per 100k)']

fig3 = px.bar(sr_sex, x='Sex', y='Suicide Rate (per 100k)', color='Sex', color_discrete_sequence=["salmon", "skyblue"], title='By Gender',
            template='simple_white')
fig3.add_hline(y=20.714, line_width=1, line_dash="dash", line_color="black")
fig3.add_hline(y=5.936, line_width=1, line_dash="dash", line_color="black")
fig3.update_layout(
        title_font_family="Courier",
        title_x=0.15)
fig3.add_annotation(xref='x',
                    yref='y',
                    axref='x',
                    ayref='y',
                    x='female', 
                    y=20,
                    showarrow=True,
                    arrowhead=1,
                    arrowwidth=3,
                    ax='female',
                    ay=5.935
                    )
fig3.add_annotation(x='female', 
                    y=13.5,
                    xshift=30,
                    text='3.5x',
                    font_size=15,
                    showarrow=False
                    )


gb_age = df.groupby('age').sum().reindex(['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years'])
sr_age = ((gb_age['suicides_no'] / gb_age['population']) * (10**5)).reset_index()
sr_age.columns = ['Age Group','Suicide Rate (per 100k)']
fig4 = px.bar(sr_age, 
            x='Age Group', 
            y='Suicide Rate (per 100k)', 
            height=400,
            color='Age Group', 
            title='By Age Group',
            color_discrete_sequence=px.colors.qualitative.Set1,
            template='simple_white')
fig4.update_layout(
        title_font_family="Courier",
        title_x=0.15)
# -------------------------------------------------------------------------------------------------------------------
# Layout

app.layout = html.Div([
    html.Div([
        html.H1(children='Exploration of Suicide Data (1985-2016)', style={'text-align':'left', 'padding': '15px 30px 15px 30px'}),
        
         # Highlights bar
        html.Div([
                html.Div([
                    html.H3('Lithuania'),
                    html.Br(),
                    html.P('Country with Highest Suicide Rate (41.18)')
                ], className='hi-lite-card'),

                html.Div([
                    html.H3('350%'),
                    html.Br(),
                    html.P('Higher Rate of Suicide Amongst Males vs. Females')
                ], className='hi-lite-card'),

                html.Div([
                    html.H3('1995'),
                    html.Br(),
                    html.P('Year With the Highest Rate of Suicide (15.3)')
                    
                ], className='hi-lite-card'),

                html.Div([
                    html.H3('75+'),
                    html.Br(),
                    html.P('Age Group with Highest Suicide Rate')
                    
                ], className='hi-lite-card')

            ], className='hi-lite-cont'),

        html.Div([
            
            # by Country
            html.Div([
                html.P('By Country, Average Rate Across Year Range', style={'font-size':'12pt', 'text-align':'left', 'padding': '5px 5px 5px 30px'}),
                dcc.Graph(
                    id = 'suicide-loc',
                    figure=fig
                )
                ], className='card'),

            # by Sex
            html.Div([
                dcc.Graph(
                    id = 'suicide-sex',
                    figure=fig3
                )
                ], className='card'),            
            # by Time
            html.Div([
                dcc.Graph(
                    id = 'suicide-time',
                    figure=fig2
                )
                ], className='card'),
            # by Age
            html.Div([
                dcc.Graph(
                    id = 'suicide-age',
                    figure=fig4
                )
                ], className='card'),

            
        ], className='dash-layout'),

        

        

    ], style={'padding':'20px','max-width': '1400px', 'margin':'auto', 'box-shadow': '0 0 0 1pt white' , 'border-radius': '2pt'})

], className='background')

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