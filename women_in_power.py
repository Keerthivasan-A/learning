import pandas as pd
import numpy as np
from functools import reduce
import plotly.express as px
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


def reduce_col_to_rows(data, content_col):
    # Melt huge list of column values to independent rows
    cols = list(data.columns)
    data = pd.melt(data,
                   id_vars=cols[:4],
                   value_vars=cols[5:])

    # Drop unnecessary columns
    data = data.drop(['Indicator Name', 'Indicator Code'], axis=1)

    # Rename columns
    data.columns = ['Country Name', 'Country Code', 'Year', content_col]

    return data


def data_wrangling(f_par_prop, f_prop, m_prop, meta_countries):
    """
    :param f_par_prop:
    :param f_prop:
    :param m_prop:
    :param meta_countries:
    :return:
    """
    # Convert columns to rows
    f_par_prop = reduce_col_to_rows(f_par_prop, 'Seats Held in National Parliment')
    f_prop = reduce_col_to_rows(f_prop, 'Female propotion')
    m_prop = reduce_col_to_rows(m_prop, 'Male propotion')

    # Change data type to string to successfully join the dataframes
    f_par_prop[['Country Name', 'Country Code', 'Year']] = f_par_prop[['Country Name', 'Country Code', 'Year']].astype(str)
    f_prop[['Country Name', 'Country Code', 'Year']] = f_prop[['Country Name', 'Country Code', 'Year']].astype(str)
    m_prop[['Country Name', 'Country Code', 'Year']] = m_prop[['Country Name', 'Country Code', 'Year']].astype(str)

    # Form the proportions data
    data = [f_par_prop, f_prop, m_prop]
    data = reduce(lambda left, right: pd.merge(left,
                                               right,
                                               on=['Country Name', 'Country Code', 'Year'],
                                               how='left'),
                  data)

    # Get countries metadata information
    data = pd.merge(data,
                    meta_countries,
                    on='Country Code',
                    how='left')
    return data


def global_trend(data):
    """
    :param data:
    :return:
    """
    world_level = data.groupby(['Year'], as_index=False).agg({'Seats Held in National Parliment': 'mean'})  # Year aggregation
    world_level = world_level[~world_level['Seats Held in National Parliment'].isnull()]  # Use only available values of proportion

    # Draw figure
    fig = px.line(world_level,
                  x='Year',
                  y='Seats Held in National Parliment',
                  template='simple_white',
                  hover_name='Year',
                  title='Average Propotion Of Seats Held By Women In National Parliment')

    # Set custom hover message
    fig.update_traces(mode="markers+lines",
                      hovertemplate="%{y:.2f} % of seats were held in %{x}")

    fig.update_layout(xaxis=dict(title='Year',
                                 linewidth=2,
                                 linecolor='black'),
                      yaxis=dict(title='% of Seats Held',
                                 range=[0, world_level['Seats Held in National Parliment'].max() + 2],
                                 linewidth=2,
                                 linecolor='black'),
                      title=dict(x=0.5)
                      )

    fig.update_layout(
        font_family="Droid Serif",
        title_font_family="Open Sans",
        legend_title_font_color="green"
    )
    return fig


def global_trend_by_cols(data):
    """

    :param data:
    :return:
    """
    df = data.groupby(['Year', 'IncomeGroup'], as_index=False).agg({'Seats Held in National Parliment': 'mean'})

    fig = px.line(df[~df['Seats Held in National Parliment'].isnull()],
                  x='Year',
                  y='Seats Held in National Parliment',
                  color='IncomeGroup',
                  template='simple_white')

    fig.update_layout(xaxis=dict(title='Year',
                                 linewidth=2,
                                 linecolor='black'),
                      yaxis=dict(title='% of Seats Held',
                                 range=[0, df['Seats Held in National Parliment'].max() + 2],
                                 linewidth=2,
                                 linecolor='black'),
                      title=dict(x=0.5)
                      )

    fig.update_layout(
        font_family="Droid Serif",
        title_font_family="Open Sans",
        legend_title_font_color="green"
    )
    return fig


def global_map(data):
    """
    :param data:
    :return:
    """
    country_level = data.groupby(['Year', 'Country Name', 'Country Code'], as_index=False).agg({'Seats Held in National Parliment': 'mean'})
    country_level = country_level[~country_level['Seats Held in National Parliment'].isnull()]  # Use only available values of proportion

    fig = px.choropleth(country_level,
                        locations="Country Code",
                        color="Seats Held in National Parliment",  # lifeExp is a column of gapminder
                        hover_name="Country Name",  # column to add to hover information
                        color_continuous_scale='OrRd',
                        template='plotly_white')
    return fig


if __name__ == "__main__":
    # Load Data
    df_f_par_prop = pd.read_excel('.\data\API_SG.GEN.PARL.ZS_DS2_en_excel_v2_1217846.xlsx')
    df_f_prop = pd.read_excel('.\data\API_SP.POP.TOTL.FE.ZS_DS2_en_csv_v2_1219499.xlsx')
    df_m_prop = pd.read_excel('.\data\API_SP.POP.TOTL.MA.ZS_DS2_en_csv_v2_1222903.xlsx')
    df_meta_countries = pd.read_excel('./data/Metadata_Country.xlsx')
    df = data_wrangling(df_f_par_prop, df_f_prop, df_m_prop, df_meta_countries)

    # Dash app
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    # dbc.Col(html.H1("Women Empowerment In Parliament"),
    #         width=3,
    #         style={'text-align': 'center'},

    app.layout = html.Div(
        [dbc.Row(
            [dbc.Col(html.H1("Women Empowerment In Parliament"),
                     style={'text-align':'center'}
                     ),
             ]
        )
        ]
    )

    app.run_server()
