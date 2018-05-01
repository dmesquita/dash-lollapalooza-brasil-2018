import plotly.graph_objs as go
import plotly.offline as offline
import pandas as pd
import numpy as np

mapbox_token = ""

df = pd.read_csv("data/data.csv")

df_markers = df.groupby(["latitude","longitude","date"]).agg(dict(product = lambda x: "%s" % ", ".join(x), hour = lambda x: "%s" % ", ".join(x)))
df_markers.reset_index(inplace=True)

data = []
update_buttons = []

dates = np.unique(df_markers["date"])

for i,date in enumerate(dates):
    df_markers_date = df_markers[df_markers["date"] == date]
    trace = go.Scattermapbox( lat = df_markers_date["latitude"], lon = df_markers_date["longitude"], name = date, text=df_markers_date["product"]+"<br>"+df_markers_date["hour"], visible=False)
    data.append(trace)

    visible_traces = np.full(len(dates), False)
    visible_traces[i] = True

    button = dict(label=date, method="restyle", args=[dict(visible = visible_traces)])
    update_buttons.append(button)

updatemenus = [dict(active=-1, buttons = update_buttons)]

layout = go.Layout(mapbox=dict(accesstoken=mapbox_token, center=dict(lat = -23.701057,lon = -46.6970635), zoom=14.5), updatemenus=updatemenus)

figure = go.Figure(data = data, layout = layout)

offline.plot(figure)

