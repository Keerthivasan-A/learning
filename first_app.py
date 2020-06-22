import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot
import streamlit as st

"""
# My first app
Here's our first attempt at using data to create a table:
"""

@st.cache  # 👈 This function will be cached
def my_slow_function():
    df = pd.DataFrame({
                  'first column': [1, 2, 3, 4],
                  'second column': [10, 20, 30, 40]
                })
    return df
df = my_slow_function()
df

x = st.sidebar.slider('x', 0, 5)  # 👈 this is a widget
st.write(x, 'squared is', x * x)

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)