#######
# Objective: Create a dashboard that takes in two or more
# input values and returns their product as the output.
######

# Perform imports here:
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Launch the application:
app = dash.Dash()

# Create a Dash layout that contains input components
# and at least one output. Assign IDs to each component:
app.layout = html.Div([
    dcc.RangeSlider(id='range_slider',
                    min=-5,
                    max=6,
                    step=1,
                    marks={value: value for value in range(-5, 6, 1)},
                    value=[-1, 1]),
    html.Div(id='multiply')
])


# Create a Dash callback:
@app.callback(Output('multiply', 'children'),
              [Input('range_slider', 'value')])
def give_selected_range(value_list):
    return value_list[0] * value_list[1]


# Add the server clause:
if __name__ == "__main__":
    app.run_server()