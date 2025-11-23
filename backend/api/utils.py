import pandas as pd
from django.core.files.storage import default_storage

def analyze_csv(file_path):
    absolute_path = default_storage.path(file_path)
    df = pd.read_csv(absolute_path)

    total_count = len(df)

    avg_flowrate = df["Flowrate"].mean()
    avg_pressure = df["Pressure"].mean()
    avg_temperature = df["Temperature"].mean()

    min_flowrate = df["Flowrate"].min()
    min_pressure = df["Pressure"].min()
    min_temperature = df["Temperature"].min()

    max_flowrate = df["Flowrate"].max()
    max_pressure = df["Pressure"].max()
    max_temperature = df["Temperature"].max()

    type_distribution = df["Type"].value_counts().to_dict()

    rows = df.head().to_dict(orient='records')
    return {
        "total_count": total_count,
        "avg_flowrate": round(avg_flowrate, 2),
        "avg_pressure": round(avg_pressure, 2),
        "avg_temperature": round(avg_temperature, 2),
        "type_distribution": type_distribution,
        "min_flowrate": round(min_flowrate,2),
        "min_pressure": round(min_pressure,2),
        "min_temperature": round(min_temperature,2),
        "max_flowrate": round(max_flowrate,2),
        "max_pressure": round(max_pressure,2),
        "max_temperature": round(max_temperature,2),
        "rows": rows,
    }
