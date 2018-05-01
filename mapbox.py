import plotly.graph_objs as go
import plotly.offline as offline
import pandas as pd

mapbox_token = ""

df = pd.read_csv("data/stages.csv")

trace = go.Scattermapbox(lat = df["latitude"], lon = df["longitude"], text=df["stage"], marker=go.Marker(size=10), mode="markers+text", textposition="top")

data = [trace]

layout = go.Layout(mapbox=dict(accesstoken=mapbox_token, center=dict(lat = -23.701057,lon = -46.6970635), zoom=14.5))

figure = go.Figure(data = data, layout = layout)

offline.plot(figure)

