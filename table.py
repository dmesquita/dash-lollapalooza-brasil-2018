import plotly.graph_objs as go
import plotly.offline as offline
import pandas as pd

df_table = pd.read_csv("data/concerts_I_attended.csv").dropna(subset=["concert"])

def colorFont(x):
    if x == "Yes":
       return "rgb(0,0,9)"
    else:
       return "rgb(178,178,178)"

df_table["color"] = df_table["correct"].apply(lambda x: colorFont(x))

trace_table = go.Table(header=dict(values=["Concert","Date","Correct?"],fill=dict(color=("rgb(82,187,47)"))),cells=dict(values=[df_table.concert,df_table.date,df_table.correct],font=dict(color=([df_table.color]))))

data = [trace_table]

figure = go.Figure(data = data)

offline.plot(figure)
