import plotly.graph_objs as go
import pandas as pd
import plotly.offline as offline

df = pd.read_csv("data/data.csv")

df_purchases_by_type = df.pivot_table(index="place",columns="date",values="price",aggfunc="sum").fillna(0)
df["hour_int"] = pd.to_datetime(df["hour"], format="%H:%M", errors='coerce').apply(lambda x: int(x.hour))

df_heatmap = df.pivot_table(index="date",values="price",columns="hour", aggfunc="sum").fillna(0)

trace_heatmap = go.Heatmap(x = df_heatmap.columns, y = df_heatmap.index, z = [df_heatmap.iloc[0], df_heatmap.iloc[1], df_heatmap.iloc[2]])

data = [trace_heatmap]

layout = go.Layout(title="Purchases by place", showlegend=True)

figure = go.Figure(data=data, layout=layout)

offline.plot(figure)

