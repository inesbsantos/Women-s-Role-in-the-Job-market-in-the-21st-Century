import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.colors as colors

#----------------------------- Style -----------------------------

# Color Palette
colors = ['#F6BD60', '#F7D5A1', '#F7EDE2', '#84A59D', '#ACCEC6', '#F28482', '#F5CAC3']

#Ver antes esta -> https://coolors.co/palette/f6bd60-f7ede2-f5cac3-84a59d-f28482


#----------------------------- Data -----------------------------

path = r'https://raw.githubusercontent.com/inesbsantos/Women-s-Role-in-the-21st-Century/main/datasets/'

# Women Business and Law datasets

df_women_business_and_law = pd.read_csv(path + 'pay.csv')

df_workplace_data = pd.read_csv(path + 'workplace.csv')

df_paid_leave = pd.read_csv(path + 'parenthood.csv')

# Labor Force Data

df_labor_force = pd.read_csv(path + 'labor_force_by_gender.csv')

# Total Population Data

df_population_by_gender = pd.read_csv(path + 'population_by_gender.csv')

# Working Age Population Data

df_working_age_population = pd.read_csv(path + 'working_age_population_ratio.csv')

# Employment Data

df_employment_to_population = pd.read_csv(path + 'employment_to_population_ratio.csv')

# Employment by sector

df_employment_by_sector_and_gender = pd.read_csv(path + 'employment_by_sector_and_gender.csv')

#------------------------- App Deployment -------------------------

# Requirements for the dash core components

country_options = [
    dict(label=country, value=country)
    for country in df_labor_force['Country'].unique()]

year_options = [
    dict(label=year, value=year)
    for year in df_employment_by_sector_and_gender['Year'].unique()]

# Donut Charts
pay_count = df_women_business_and_law[df_women_business_and_law['Report Year']==2023].groupby('Does the law mandate equal remuneration for work of equal value?').count()['Economy']

donut_chart_pay_fig = go.Figure(data=[go.Pie(labels=df_women_business_and_law['Does the law mandate equal remuneration for work of equal value?'].unique(), 
                                             values=pay_count, 
                                             hole=.6,
                                             marker=dict(colors=[colors[4], colors[6]]))])

title1_num = str(pay_count['Yes'])
title1 = 'mandate equal remuneration for work of equal value' 

law_against_discrimination_count = df_workplace_data[df_workplace_data['Report Year']==2023].groupby('Does the law prohibit discrimination in employment based on gender?').count()['Economy']

donut_chart_discrimination_fig = go.Figure(data=[go.Pie(labels=df_workplace_data['Does the law prohibit discrimination in employment based on gender?'].unique(), 
                                             values=law_against_discrimination_count, 
                                             hole=.6,
                                             marker=dict(colors=[colors[4], colors[6]]))])

title2_num = str(law_against_discrimination_count['Yes'])
title2 ='prohibit discrimination in employment based on gender' 

dismissal_preg_workers_count = df_paid_leave[df_paid_leave['Report Year']==2023].groupby('Is dismissal of pregnant workers prohibited?').count()['Economy']

donut_chart_dismissal_preg_workers_fig = go.Figure(data=[go.Pie(labels=df_paid_leave['Is dismissal of pregnant workers prohibited?'].unique(), 
                                             values=dismissal_preg_workers_count, 
                                             hole=.6,
                                             marker=dict(colors=[colors[4], colors[6]]))])

title3_num = str(dismissal_preg_workers_count['Yes'])
title3 ='prohibit the dismissal of pregnant workers' 

# Maps
industrial_jobs_count = df_women_business_and_law.groupby(['Can a woman work in an industrial job in the same way as a man?', 'Report Year']).count()['Economy']

x = industrial_jobs_count.Yes[2001]
y = industrial_jobs_count.Yes[2023]

df_women_business_and_law= df_women_business_and_law.replace('No',0)
df_women_business_and_law = df_women_business_and_law.replace('Yes',1)

data_choropleth = dict(type='choropleth',
                       locations=df_women_business_and_law['Economy'].unique(), 
                       locationmode='country names',
                       z=df_women_business_and_law[df_women_business_and_law['Report Year']==2023]['Can a woman work in an industrial job in the same way as a man?'],
                       text=df_women_business_and_law['Economy'].unique(),
                       colorscale=[colors[2], colors[5]],
                       showscale=False
                      )

layout_choropleth = dict(geo=dict(scope='world',  #default
                                  projection=dict(type='orthographic'
                                                 ),
                                  showland=True,   
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True, 
                                  oceancolor='azure'
                                 )
                        )

map2023 = go.Figure(data=data_choropleth, layout=layout_choropleth)

data_choropleth2 = dict(type='choropleth',
                       locations=df_women_business_and_law['Economy'].unique(), 
                       locationmode='country names',
                       z=df_women_business_and_law[df_women_business_and_law['Report Year']==2001]['Can a woman work in an industrial job in the same way as a man?'],
                       text=df_women_business_and_law['Economy'].unique(),
                       colorscale=[colors[2], colors[5]],
                       showscale=False
                      )

layout_choropleth2 = dict(geo=dict(scope='world',  #default
                                  projection=dict(type='orthographic'
                                                 ),
                                  showland=True,   
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True, 
                                  oceancolor='azure'
                                 )
                        )

map2001 = go.Figure(data=data_choropleth2, layout=layout_choropleth2)

#The app itself

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Add reference to custom CSS file(s)
app.css.append_css({
    'external_url': '/assets/typography.css'  
})

app.css.append_css({
    'external_url': '/assets/graphs.css'  
})

app.css.append_css({
    'external_url': '/assets/header.css'  
})

server = app.server

app.layout = html.Div([

    html.Header("Women's Role in the Job Market in the 21st Century"),

    html.Div(id='h_bar'),

    html.P(id="intro", children="People tend to think of gender discrimination as a thing from the past. However, its effects still linger to this day, and it is important to be aware of this issue so as to not repeat past mistakes."),

    html.Div(
            [
                dbc.Row(id="firstRow", children=
                [
                    html.H2("In 2023, out of 190 Countries..."),

                    dbc.Col(html.Div([
                            dcc.Graph(id='donut_chart_discrimination',
                                    figure=donut_chart_discrimination_fig), 
                        
                            html.H5(className='graphtitle',children=[
                                html.P(className="bold", children=title2_num),
                                html.P(title2)
                            ])  
                    ])),

                    dbc.Col(html.Div([
                            dcc.Graph(id='donut_chart_paid_leave',
                                    figure=donut_chart_dismissal_preg_workers_fig),

                            html.H5(className='graphtitle',children=[
                                html.P(className="bold", children=title3_num),
                                html.P(title3)
                            ]) 
                        ])),

                    dbc.Col(html.Div([
                            dcc.Graph(id='donut_chart_pay',
                                    figure=donut_chart_pay_fig),

                            html.H5(className='graphtitle',children=[
                                html.P(className="bold", children=title1_num),
                                html.P(title1)
                            ])              
                        ])),
                    
                ]),

                dbc.Row(id="secondRow", children=
                [
                    html.H2("And There are still gender disparities in labor force participation"),

                    html.Div(className='dropdown-right',children=[
                        dcc.Dropdown(
                                id='country_drop1',
                                className='country_drop',
                                options=country_options,
                                value='World',
                                multi=False
                            ), 
                    ]),

                    dcc.Graph(id="wage_line_chart"),

                    dcc.RangeSlider(
                            id='year_slider',
                            min=2001,
                            max=2020,
                            value=[2001, 2020],
                            marks={'2001': '2001',
                                '2005': '2005',
                                '2010': '2010',
                                '2015': '2015',
                                '2020': '2020'},
                            step=1
                        )
                ]),

                dbc.Row(id="thirdRow", children=
                [
                    html.H2("But differences can be more noticeable depending on the sector"),
                    
                    dbc.Col(html.Div([
                        dcc.Graph(id="employment_by_sector_bar_chart"),
                    ]), width=7),

                    dbc.Col(html.Div([
                        html.Div(id="p2",children=[
                            html.H4("1."),
                            html.P("From the three main economic activities, women tend to gravitate more towards the Services sector, while their presence in the Agriculture sector has noticeably decreased since the beginning of the 21st Century. In contrast, the proportion of employed women in the industry sector has remained almost immutable.")
                            ]),
                            html.Br(),
                            dcc.Dropdown(
                                    id='country_drop2',
                                    options=country_options,
                                    value='World',
                                    multi=False
                                ),
                    ]))
                ]),

                dbc.Row(id="fourthRow", children=
                [
                    dbc.Col(html.Div(id='p1',children=[
                        html.H4("2."),
                        html.P("While this drop in the Agriculture sector is more of a global phenomenon independent of gender, there are clear gender disparities in the Services and Industry sectors, with women being more concentrated in the former, and men in the latter. Not only that, but there's less unemployment among men of working age."),
                        html.Br(),

                        dcc.Dropdown(
                                id='year_drop',
                                options=year_options,
                                value=2019,
                                multi=False
                            ),
                    ])),

                    dbc.Col(html.Div([
                        dcc.Graph(id="sunburst_sectors"),
                    ]), width=8),
                ]),

                dbc.Row(id="fifthRow", children=
                [
                    html.H2("So what is happening in the Industry sector?"),

                    html.Br(),

                    html.P(children=["The industry sector consists of activities such as mining and quarrying, manufacturing, construction, and public utilities. The ever-present gender discrepancy in this sector may be due to countries' legislations."], id="industrydesc"),

                    html.H4("Countries Where Women can Work in an Industrial Job in the Same Way as a Man"),
                    
                    dbc.Col(html.Div([
                        html.H5("2001"),
                        html.P(["Only ",
                                html.Span(str(x), style={'font-weight': 'bold'}),
                                " countries had legislation that allowed women to work in industrial jobs int the same way as a man."]),
                        dcc.Graph(id="map2001", figure=map2001)
                    ])),

                    dbc.Col(html.Div([
                        html.H5("2023"),
                        html.P(["This number has now increased to ",
                                html.Span(str(y), style={'font-weight': 'bold'}),
                                ", with Portugal now being one of them."]),
                        dcc.Graph(id="map2023", figure=map2023)
                    ])),

                ]),
            ]),

    html.Br(),
    html.Hr(),
    html.P(children=[
            html.B("Authors: "),
            html.P("Ana Beatriz Estevez, r20191209 | Filipe Dias, r20181050 | Inês Santos, r20191184 | Manuel Marreiros, r20191223"),
            html.Br(),
            html.P("NOVA IMS 2023")
            ], style={"text-align":"center"})
])

@app.callback(
    [Output('wage_line_chart', 'figure'),
     Output('employment_by_sector_bar_chart', 'figure'),
     Output('sunburst_sectors','figure')],
    [Input('country_drop1', 'value'),
     Input('year_slider', 'value'),
     Input('country_drop2', 'value'),
     Input('year_drop', 'value')],

)

def update_graph(country, year, country2, year2):

    # Wage scatter plot

    filtered_by_country = df_labor_force[df_labor_force['Country']==country]

    filtered_by_year = filtered_by_country[(filtered_by_country['Year'] >= year[0]) & (filtered_by_country['Year'] <= year[1])]   

    scatter_data = []

    colors_custom = [colors[3], colors[5], colors[0]]

    for indicator in filtered_by_year['Indicator'].unique():
        final_df = filtered_by_year[filtered_by_year['Indicator']==indicator]

        temp_data = dict(
                type='scatter',
                y=final_df['Value'],
                x=final_df['Year'],
                name=indicator
            )
        
        scatter_data.append(temp_data)

    scatter_layout = dict(plot_bgcolor='#FFFFFF', 
                      xaxis=dict(
                        gridcolor='lightgrey',
                        gridwidth=0.5,
                        title='Year'
                      ),
                      yaxis=dict(
                          gridcolor='lightgrey',
                          gridwidth=0.5,
                          title='Percentage'),
                      colorway= colors_custom
                     )
    
    fig1 = go.Figure(data=scatter_data, layout=scatter_layout)

    # Employment by Sector Bar Chart

    employment_by_sector_fig = go.Figure()

    filtered_to_world_df = df_employment_by_sector_and_gender[df_employment_by_sector_and_gender['Country']==country2]

    # Agriculture
    employment_by_sector_fig.add_trace(go.Bar(
        y=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment agriculture, female (%)']['Value'],
        x=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment agriculture, female (%)']['Year'],
        name='Agriculture',
        marker=dict(
            color=colors[1],
            line=dict(color=colors[0], width=3)
        )
    ))

    # Industry

    employment_by_sector_fig.add_trace(go.Bar(
        y=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment industry, female (%)']['Value'],
        x=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment industry, female (%)']['Year'],
        name='Industry',
        marker=dict(
            color=colors[4],
            line=dict(color=colors[3], width=3)
        )
    ))

    #Services

    employment_by_sector_fig.add_trace(go.Bar(
        y=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment services, female (%)']['Value'],
        x=filtered_to_world_df[filtered_to_world_df['Indicator']=='Employment services, female (%)']['Year'],
        name='Services',
        marker=dict(
            color=colors[6],
            line=dict(color=colors[5], width=3)
        )
    ))

    employment_by_sector_fig.update_layout(barmode='stack', 
                                        plot_bgcolor='#FFFFFF', 
                                        xaxis=dict(
                                                gridcolor='lightgrey',
                                                gridwidth=0.5,
                                            ),
                                            yaxis=dict(
                                                gridcolor='lightgrey',
                                                gridwidth=0.5,
                                            ),
                                            title={
                                                'text': 'Evolution of the Proportion of Employed Women By Sector',
                                                'font': {
                                                    'size': 22,
                                                    'color': 'rgb(82, 79, 79)',
                                                    'family': 'Avenir',
                                                },
                                                'x': 0.5,
                                                'y': 0.9, 
                                                'xanchor': 'center',
                                                'yanchor': 'top', 
                                            })

    # Sunburst chart

    filtered_by_country_tot_pop = df_population_by_gender[df_population_by_gender['Country']==country2]
    filtered_by_country_and_year_tot_pop = filtered_by_country_tot_pop[filtered_by_country_tot_pop['Year']==year2]
    filtered_by_country_and_year_tot_pop_female = filtered_by_country_and_year_tot_pop[filtered_by_country_and_year_tot_pop['Indicator']=='Total Population, female (%)']
    filtered_by_country_and_year_tot_pop_male = filtered_by_country_and_year_tot_pop[filtered_by_country_and_year_tot_pop['Indicator']=='Total Population, male (%)']

    filtered_by_country_pop = df_working_age_population[df_working_age_population['Country']==country2]
    filtered_by_country_and_year_pop = filtered_by_country_pop[filtered_by_country_pop['Year']==year2]
    filtered_by_country_and_year_pop_female = filtered_by_country_and_year_pop[filtered_by_country_and_year_pop['Indicator']=='Population, female (%)']
    filtered_by_country_and_year_pop_male = filtered_by_country_and_year_pop[filtered_by_country_and_year_pop['Indicator']=='Population, male (%)']

    filtered_by_country_employment = df_employment_to_population[df_employment_to_population['Country']==country2]
    filtered_by_country_and_year_employment = filtered_by_country_employment[filtered_by_country_employment['Year']==year2]
    filtered_by_country_and_year_employment_female = filtered_by_country_and_year_employment[filtered_by_country_and_year_employment['Indicator']=='Employment to population, female (%)']
    filtered_by_country_and_year_employment_male = filtered_by_country_and_year_employment[filtered_by_country_and_year_employment['Indicator']=='Employment to population, male (%)']

    filtered_by_country_sector = df_employment_by_sector_and_gender[df_employment_by_sector_and_gender['Country']==country2]
    filtered_by_country_and_year_sector = filtered_by_country_sector[filtered_by_country_sector['Year']==year2]
    filtered_by_country_and_year_agriculture_female = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment agriculture, female (%)']
    filtered_by_country_and_year_agriculture_male = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment agriculture, male (%)']
    filtered_by_country_and_year_industry_female = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment industry, female (%)']
    filtered_by_country_and_year_industry_male = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment industry, male (%)']
    filtered_by_country_and_year_services_female = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment services, female (%)']
    filtered_by_country_and_year_services_male = filtered_by_country_and_year_sector[filtered_by_country_and_year_sector['Indicator']=='Employment services, male (%)']

    female_pop = filtered_by_country_and_year_tot_pop_female['Value'].iloc[0]
    male_pop = filtered_by_country_and_year_tot_pop_male['Value'].iloc[0]

    working_age_pop_female = (filtered_by_country_and_year_pop_female['Value'].iloc[0]/100) * female_pop
    non_working_age_pop_female = ((100-filtered_by_country_and_year_pop_female['Value'].iloc[0])/100) * female_pop
    working_age_pop_male = (filtered_by_country_and_year_pop_male['Value'].iloc[0]/100) * male_pop
    non_working_age_pop_male = ((100-filtered_by_country_and_year_pop_male['Value'].iloc[0])/100) * male_pop

    employed_women_of_working_age = (filtered_by_country_and_year_employment_female['Value'].iloc[0]/100) * working_age_pop_female
    employed_men_of_working_age = (filtered_by_country_and_year_employment_male['Value'].iloc[0]/100) * working_age_pop_male
    unemployed_women_of_working_age = ((100-filtered_by_country_and_year_employment_female['Value'].iloc[0])/100) * working_age_pop_female
    unemployed_men_of_working_age = ((100-filtered_by_country_and_year_employment_male['Value'].iloc[0])/100) * working_age_pop_male

    employed_women_in_agriculture = (filtered_by_country_and_year_agriculture_female['Value'].iloc[0]/100) * employed_women_of_working_age
    employed_men_in_agriculture = (filtered_by_country_and_year_agriculture_male['Value'].iloc[0]/100) * employed_men_of_working_age

    employed_women_in_industry = (filtered_by_country_and_year_industry_female['Value'].iloc[0]/100) * employed_women_of_working_age
    employed_men_in_industry = (filtered_by_country_and_year_industry_male['Value'].iloc[0]/100) * employed_men_of_working_age

    employed_women_in_services = (filtered_by_country_and_year_services_female['Value'].iloc[0]/100) * employed_women_of_working_age
    employed_men_in_services = (filtered_by_country_and_year_services_male['Value'].iloc[0]/100) * employed_men_of_working_age

    employment_chart = go.Figure()

    employment_chart.add_traces(go.Sunburst(ids=['Female Population',
                                                'Male Population',
                                                'Working Age Population, Female',
                                                'Working Age Population, Male',
                                                'Non-Working Age Population, Female',
                                                'Non-Working Age Population, Male',
                                                'Employed Women of Working Age',
                                                'Employed Men of Working Age',
                                                'Unemployed Women of Working Age',
                                                'Unemployed Men of Working Age',
                                                'Employed women in the agriculture sector',
                                                'Employed men in the agriculture sector',
                                                'Employed women in the industry sector',
                                                'Employed men in the industry sector',
                                                'Employed women in the services sector',
                                                'Employed men in the services sector'],
                                            
                                            labels=['Female Population',
                                                    'Male Population',
                                                    'Working Age Population, Female',
                                                    'Working Age Population, Male',
                                                    'Non-Working Age Population, Female',
                                                    'Non-Working Age Population, Male',
                                                    'Employed Women',
                                                    'Employed Men',
                                                    'Unemployed Women',
                                                    'Unemployed Men',
                                                    'Agriculture',
                                                    'Agriculture',
                                                    'Industry',
                                                    'Industry',
                                                    'Services',
                                                    'Services'],
                                            parents=['',
                                                    '',
                                                    'Female Population',
                                                    'Male Population',
                                                    'Female Population',
                                                    'Male Population',
                                                    'Working Age Population, Female',
                                                    'Working Age Population, Male',
                                                    'Working Age Population, Female',
                                                    'Working Age Population, Male',
                                                    'Employed Women of Working Age',
                                                    'Employed Men of Working Age',
                                                    'Employed Women of Working Age',
                                                    'Employed Men of Working Age',
                                                    'Employed Women of Working Age',
                                                    'Employed Men of Working Age'],
                                            values=[0,
                                                    0,
                                                    0,
                                                    0,
                                                    non_working_age_pop_female,
                                                    non_working_age_pop_male,
                                                    0,
                                                    0,
                                                    unemployed_women_of_working_age,
                                                    unemployed_men_of_working_age,
                                                    employed_women_in_agriculture,
                                                    employed_men_in_agriculture,
                                                    employed_women_in_industry,
                                                    employed_men_in_industry,
                                                    employed_women_in_services,
                                                    employed_men_in_services],
                                                    
                                            leaf={'opacity': 0.8},
                                            marker=dict(colors=['#F28482', 
                                                                '#84A59D', 
                                                                '#F4A7A3', 
                                                                '#98BAB2', 
                                                                colors[2],
                                                                colors[2], 
                                                                '#F5CAC3', 
                                                                '#ACCEC6',
                                                                colors[2],
                                                                colors[2]]),
                                            hovertemplate='%{id}'))

    employment_chart.update_traces(textinfo="label+percent parent")

    employment_chart.update_layout(
        title={
            'text': 'Employment Based on Gender and Sector',
            'font': {
                'size': 22,
                'color': 'rgb(82, 79, 79)',
                'family': 'Avenir',
            },
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
        },
        height=850,
        width=950,
    )

    return [fig1, employment_by_sector_fig, employment_chart]

if __name__ == '__main__':
    app.run_server(debug=True)
