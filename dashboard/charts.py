import pandas as pd
import plotly.express as px



def create_dataframe(data):

    return pd.DataFrame(
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



def vehicle_chart(data):

    df = create_dataframe(data)

    vehicle_count = (
        df["Vehicle"]
        .value_counts()
        .reset_index()
    )


    vehicle_count.columns = [
        "Vehicle",
        "Count"
    ]


    fig = px.bar(
        vehicle_count,
        x="Vehicle",
        y="Count",
        title="Vehicle Analytics"
    )

    return fig



def density_chart(data):

    df = create_dataframe(data)


    density_count = (
        df["Density"]
        .value_counts()
        .reset_index()
    )


    density_count.columns = [
        "Density",
        "Count"
    ]


    fig = px.pie(
        density_count,
        names="Density",
        values="Count",
        title="Traffic Density"
    )


    return fig



def speed_chart(data):

    df = create_dataframe(data)


    fig = px.histogram(
        df,
        x="Speed",
        title="Vehicle Speed Analysis"
    )


    return fig



def violation_chart(data):

    df = create_dataframe(data)


    violation_count = (
        df["Violation"]
        .value_counts()
        .reset_index()
    )


    violation_count.columns=[
        "Violation",
        "Count"
    ]


    fig = px.bar(
        violation_count,
        x="Violation",
        y="Count",
        title="Traffic Violations"
    )


    return fig