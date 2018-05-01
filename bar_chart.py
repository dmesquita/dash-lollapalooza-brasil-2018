import plotly.graph_objs as go
import pandas as pd
import plotly.offline as offline

df = pd.read_csv("data/data.csv")

df_purchases_by_type = df.pivot_table(index="place",columns="date",values="price",aggfunc="sum").fillna(0)

trace_microbar = go.Bar(x = df_purchases_by_type.columns, y = df_purchases_by_type.loc["MICROBAR"])

data = [trace_microbar]

layout = go.Layout(title="Purchases by place", showlegend=True)

figure = go.Figure(data=data, layout=layout)

offline.plot(figure)

