import pandas as pd
import plotly.express as px
from pathlib import Path

from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# Locate the project's `data` directory by searching ancestors
base = None
for p in Path(__file__).resolve().parents:
    if (p / "data").exists():
        base = p
        break
if base is None:
    raise FileNotFoundError("Could not locate 'data' directory in any parent directories.")
DATA_PATH = base / "data" / "cleaned_car_data.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Data file not found at {DATA_PATH}. Please check the path.")
df = pd.read_csv(DATA_PATH)

app = Dash(__name__)

app.layout = html.Div([

    html.H1("Used Car Market Dashboard"),

    dcc.Dropdown(
        id="fuel_filter",
        options=[
            {"label": fuel, "value": fuel}
            for fuel in df["fuel_type"].unique()
        ],
        multi=True,
        placeholder="Select Fuel Type"
    ),

    dcc.Graph(id="price_chart")

])

@app.callback(
    Output("price_chart", "figure"),
    Input("fuel_filter", "value")
)

def update_chart(selected_fuels):

    filtered_df = df.copy()

    if selected_fuels:
        filtered_df = filtered_df[
            filtered_df["fuel_type"].isin(selected_fuels)
        ]

    fig = px.scatter(
        filtered_df,
        x="year",
        y="Price",
        color="fuel_type"
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)