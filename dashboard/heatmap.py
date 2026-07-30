import pandas as pd
import plotly.express as px



def vehicle_heatmap(data):

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Session",
            "Vehicle",
            "Speed",
            "Violation",
            "Density",
            "Entry",
            "Exit",
            "Timestamp"
        ]
    )


    heatmap_data = (
        df.groupby(
            ["Density", "Vehicle"]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )


    fig = px.density_heatmap(
        heatmap_data,
        x="Vehicle",
        y="Density",
        z="Count",
        title="Traffic Density Heatmap"
    )


    return fig