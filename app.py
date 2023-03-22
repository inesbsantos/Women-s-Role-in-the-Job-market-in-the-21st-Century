import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import wbgapi as wb

#----------------------------- Style -----------------------------

# Color Palette
colors = ['#F88FB0', '#F3B6C9', '#69A5E1', '#A7D1FA', '#F7A863', '#FFCEA2']

# Define font family, size, and color
font_family = "Helvetica, sans-serif"
font_size = 16
font_color = colors[0]

# Create font dictionary
font_dict = dict(family=font_family, size=font_size, color=font_color)

#----------------------------- Data -----------------------------

path = r'https://raw.githubusercontent.com/inesbsantos/Women-s-Role-in-the-21st-Century/main/datasets/'

df_female_management_employment = pd.read_csv(path + 'female_management_employment.csv')

df_female_parliament = pd.read_csv(path + 'female_parliament.csv')

df_female_day2day = pd.read_csv(path + 'female_day2day.csv')

#------------------------- App Deployment -------------------------

# Requirements for the dash core components

country_options = [
    dict(label=country, value=country)
    for country in df_female_management_employment['Country'].unique()]


#The app itself
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Women's Role in the 21st Century"),

    dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    ),

    html.Br(),

])

if __name__ == '__main__':
    app.run_server(debug=True)