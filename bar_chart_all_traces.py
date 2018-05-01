import plotly.graph_objs as go
import pandas as pd
import plotly.offline as offline

df = pd.read_csv("data/data.csv")

df_purchases_by_place = df.pivot_table(index="place",columns="date",values="price",aggfunc="sum").fillna(0)

data = []

for index,place in df_purchases_by_place.iterrows():
    trace = go.Bar(x = df_purchases_by_place.columns, y = place, name=index)
    data.append(trace)

layout = go.Layout(title="Purchases by place", showlegend=True, barmode="stack")

figure = go.Figure(data=data, layout=layout)

offline.plot(figure)

