import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

data = pd.read_excel('API_SG.GEN.PARL.ZS_DS2_en_excel_v2_1217846.xlsx', sheet_name='Data')
meta_countries = pd.read_excel('API_SG.GEN.PARL.ZS_DS2_en_excel_v2_1217846.xlsx', sheet_name='Metadata_Countries')


def world_level(df):
    """
    :param df:
    :return:
    """
    world_level = data.groupby(['Year'], as_index=False).agg({'Seats Held in National Parliment': 'mean'})  # Year aggregation
    world_level = world_level[~world_level['Seats Held in National Parliment'].isnull()]  # Use only available values of proportion

    # Annotation
    x_annot, y_annot = world_level[world_level['Year'] == world_level['Year'].min()][['Year', 'Seats Held in National Parliment']].values.tolist()[0]

    # Draw figure
    fig = px.line(world_level,
                  x='Year',
                  y='Seats Held in National Parliment',
                  template='simple_white',
                  hover_name='Year',
                  title='Average propotion of seats held by women in national parliment'
                  )

    # Set custom hover message
    fig.update_traces(mode="markers+lines",
                      hovertemplate="%{y:.2f} % of seats were held in %{x}"
                      )

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