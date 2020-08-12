import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

from scipy import stats
from scipy.stats import f_oneway
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from statsmodels.formula.api import ols
from plotly.subplots import make_subplots

"""
Continuous variable
"""

def get_central_tendency(df, col_name):
    """
    df: Input data frame
    col_name: Column name in the input dataframe
    """
    if col_name in df.columns:
        arguments = {'mean': df[col_name].mean(),
                     'median': df[col_name].median(),
                     'mode': stats.mode(df[col_name]),
                     'min': df[col_name].min(),
                     'max': df[col_name].max(),
                     'skew': df[col_name].skew(),
                     'kurtosis': df[col_name].kurtosis(),
                     'std': df['salary'].std(),
                     'var': df['salary'].var(),
                     '25th_perc': df['salary'].quantile(0.25),
                     '75th_perc': df['salary'].quantile(0.75),
                     'IQR': stats.iqr(df.loc[~df[col_name].isnull(), col_name])
                     }

        print("\n -----------CENTRAL TENDENCY OF {}-----------".format(str(col_name).upper()))
        print("""\n Mean: {mean} 
                 \n Median: {median} 
                 \n Mode: {mode}
                 \n Skewness: {skew}
                 \n Kurtosis: {kurtosis}
              """.format(**arguments))

        print("\n -----------MEASURE OF DISPERSION OF {}-----------".format(str(col_name).upper()))
        print("""\n Standard deviation: {std} 
                 \n Variance: {var}
                 \n Range of values: {min} - {max}
                 \n Inter quartile range: {IQR}
                 \n 25th Percentile: {25th_perc}
                 \n 75th Percentile: {75th_perc}
              """.format(**arguments))

    else:
        print("Requested column not in the given dataframe")


def get_ecdf(df, col_name):
    """
    Plot the emprical distributed value of a continuos variable
    df: Input data frame
    col_name: Column name in the input dataframe
    """
    x = np.empty([0])
    y = np.empty([0])
    if col_name in df.columns:
        x = np.sort(np.sort(df[col_name]))
        n = x.size
        y = np.arange(1, n + 1) / n
    else:
        print("Requested column not in the given dataframe")
    return x, y


def plot_all_distribution(df, col_name):
    """
    Plot the histogram, boxplot and ECDF
    """
    if col_name in df.columns:
        # Subplots
        fig = make_subplots(rows=1,
                            cols=3)

        # Plot histogram
        fig.add_trace(go.Histogram(x=df[col_name],
                                   name='Histogram'),
                      row=1,
                      col=1)

        # Plot box plot
        fig.add_trace(go.Box(y=df[col_name],
                             boxpoints='all',
                             name='Boxplot'),
                      row=1,
                      col=2)

        # Plot ECDF function
        x, y = get_ecdf(df, col_name)
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 mode='markers',
                                 name='ECDF'),
                      row=1,
                      col=3)

        fig.update_layout(title={'text': "{} VARIABLE DISTRIBUTION".format(str(col_name).upper()),
                                 'x': 0.5})

        fig.show()


"""
Categorical variable
"""
def get_frequency_table(df, col_name):
    """
    Returns frequency table
    """
    if col_name in df.columns:
        # Absolute frequency
        cat_frequency = df['specialisation'].value_counts().reset_index()

        # Column rename
        cat_frequency.rename(columns={'index': 'specialisation',
                                      'specialisation': 'Absolute frequency'},
                             inplace=True)

        # Absolute frequency (in percentage)
        cat_frequency['Relative frequency (%)'] = (cat_frequency['Absolute frequency'] /
                                                   cat_frequency['Absolute frequency'].sum()) * 100

        return cat_frequency.sort_values(['Absolute frequency'], ascending=False)

    else:
        print("Requested column not in the given dataframe")


def plot_cat_data(df_frequency, col_name):
    """
    Plot frequency distribution as bar chart
    df_frequency: Input data frame with value counts and %
    col_name: Column name in the input dataframe
    """
    # Create 2 columns plots
    fig = make_subplots(rows=1,
                        cols=2)

    # Plot value count in bar chart in first plot
    fig.add_trace(go.Bar(x=df_frequency[col_name],
                         y=df_frequency['Absolute frequency'],
                         text=df_frequency['Absolute frequency'],
                         name='Absolute frequency'),
                  row=1,
                  col=1)

    # Plot % of value count in bar chart in second plot
    fig.add_trace(go.Bar(x=df_frequency[col_name],
                         y=df_frequency['Relative frequency (%)'],
                         text=df_frequency['Relative frequency (%)'],
                         texttemplate='%{text:.2f}' + "%",
                         name='Relative frequency %'),
                  row=1,
                  col=2)

    fig.update_traces(textposition='outside')
    fig.update_layout(title={'text': "{} FREQUENCY DISTRIBUTION".format(str(col_name).upper()),
                             'x': 0.5})
    fig.show()


def continuous_bivariate(df, col_list):
    """
    Find the relation between 2 numerical cols by ploting scatter plot and pearson co-efficient matrix
    Data: Input data frame
    col_list: list of numerical cols
    """
    # Get Correlation matrix
    corr_matrix = df[col_list].corr()
    corr_matrix = corr_matrix.round(3)

    fig = ff.create_annotated_heatmap(z=corr_matrix.values,
                                      x=list(corr_matrix.columns),
                                      y=list(corr_matrix.index),
                                      colorscale='Reds',
                                      annotation_text=corr_matrix.values,
                                      showscale=True
                                      )
    fig.update_layout(title={'text': 'Pearson correlation Matrix',
                             'x': 0.5},
                      height=500,
                      width=800)

    fig.show()

    # Get scatterplot corelation
    fig = px.scatter_matrix(df, dimensions=col_list, color='status')

    fig.update_layout(title={'text': 'Scatter plot correlation Matrix',
                             'x': 0.5})
    fig.show()


def get_f_stats(df, numerical_col, nominal_col, annova_type=1):
    """
    Do ANNOVA test and get F statistics
    df: input data
    numerical_col: Name of the numerical col in df
    nominal_col: Name of the nominal/categorical col in df
    """
    if not df.empty:
        # Method 1
        query_args = {'numerical_col': numerical_col,
                      'nominal_col': nominal_col}
        mod = ols('{numerical_col} ~ {nominal_col}'.format(**query_args), data=df).fit()
        print(sm.stats.anova_lm(mod, typ=annova_type))

        # Method 2
        # groups = {each_status: df.loc[df.status == each_status, 'degree_p'].values for each_status in data.status.unique()}
        # f_oneway(groups['Placed'], groups['Not Placed'])


def get_chi_stats(df, nominal_col1, nominal_col2):
    """
    Do Chi sqaured test of independence
    df: input data
    nominal_col1: Name of the nominal/categorical col in df
    nominal_col2: Name of the nominal/categorical col in df
    """
    if not df.empty:
        observed = pd.crosstab(index=df[nominal_col1],
                               columns=df[nominal_col2],
                               margins=True,
                               margins_name='Total')
        chi2_value, p_value, degree_of_freedom, expected = chi2_contingency(observed, correction=False)
        print("Chi Statistics", chi2_value,
              "\nProbability value", p_value,
              "\nDegree of freedom", degree_of_freedom)
