import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
 
app = dash.Dash()

mapbox_token = ""

df = pd.read_csv("data.csv")
df_stages = pd.read_csv("stages.csv")

df_markers = df.groupby(["latitude","longitude","date"]).agg(dict(product = lambda x: "%s" % ", ".join(x), hour = lambda x: "%s" % ", ".join(x)))
df_markers.reset_index(inplace=True)

buttons_map = []
data_map = []

# add markers for stages
data_map.append(
    go.Scattermapbox(
        lat = df_stages["latitude"],
        lon = df_stages["longitude"],
        text = df_stages["stage"],
        mode = 'markers+text',
        name = 'Stages',
        marker = go.Marker(size=15,color="rgb(187,86,167)"),
        textposition = "top",
        textfont = dict(color="black"),
        hoverinfo="text+name",
        showlegend = False 
    )
)

# add markers for all purchases
data_map.append(    
    go.Scattermapbox(
        lat = df_markers["latitude"],
        lon = df_markers["longitude"],
        text = df_markers["product"]+"<br>"+df_markers["hour"],
        mode = 'markers',
        name = 'All days',
        hoverinfo ="text",
        marker = go.Marker(size=7)
    )
)

dates = np.unique(df_markers["date"])

visible_traces = np.full(len(dates)+2, False)
visible_traces[0] = True 
visible_traces[1] = True 

buttons_map.append(
   dict(
       label="All days",
       method="restyle",
       args=[{'title':'All','visible':visible_traces}]
   )
)

for i,date in enumerate(dates):
    df_markers_date = df_markers[df_markers["date"] == date]
    trace = go.Scattermapbox( 
        lat = df_markers_date["latitude"], 
        lon = df_markers_date["longitude"], 
        name = date,
        hoverinfo = "text", 
        text=df_markers_date["product"]+"<br>"+df_markers_date["hour"], 
        visible=False,
        marker = go.Marker(size = 7)
      )
    data_map.append(trace)

    visible_traces = np.full(len(dates)+2, False)
    visible_traces[0] = True 
    visible_traces[i+2] = True

    button = dict(label=date, method="restyle", args=[dict(visible = visible_traces)])
    buttons_map.append(button)

updatemenus = [dict(buttons = buttons_map)]

layout_map = go.Layout(
    autosize = True,
    margin = dict(t=30,b=30),
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_token,
        bearing=0,
        center=dict(
            lat=-23.701057,
            lon=-46.6970635
        ),
        pitch=0,
        zoom=14.5
    ),
    updatemenus=updatemenus,
    showlegend=False
)

figure_map = go.Figure(data = data_map, layout = layout_map)

df["type"] = df["product"].apply(lambda val: ("beverage" if val in ["Cerveja Bud","Spirit", "Cerveja Beats", "Água"] else "food"))
df_food_type = df.pivot_table(index="type",columns="date",values="price",aggfunc="sum")

data_food_type = []

for food in df_food_type.index:
    if food == "beverage":
        color = "rgb(0,161,159)"
    else:
        color = "rgb(238,0,140)"
    trace = go.Bar(y = df_food_type.loc[food], x = df_food_type.columns, name=food,marker=dict(color=color))
    data_food_type.append(trace)

layout_food_type = go.Layout(showlegend=True, barmode="stack", margin=dict(l=30,t=30))

figure_food_type = go.Figure(data = data_food_type, layout = layout_food_type)

df_heatmap = df.pivot_table(index="date",values="price",columns="hour", aggfunc="sum").fillna(0)

trace_heatmap = go.Heatmap(
    x = df_heatmap.columns, 
    y = df_heatmap.index, 
    z = [df_heatmap.iloc[0], df_heatmap.iloc[1], df_heatmap.iloc[2]],
    colorscale = [[0.0, 'rgb(240,241,243)'], [0.20, 'rgb(239,179,208)'],[1.0, 'rgb(146,28,136)']]
)

data_heatmap = [trace_heatmap]

layout_heatmap = go.Layout(margin = dict(l=80, t=30))

figure_heatmap = go.Figure(data = data_heatmap, layout = layout_heatmap)

df_table = pd.read_csv("concerts_I_attended.csv").dropna(subset=["concert"])
def colorFont(x):
    if x == "Yes":
       return "rgb(0,0,9)"
    else:
       return "rgb(178,178,178)"

df_table["color"] = df_table["correct"].apply(lambda x: colorFont(x))

trace_table = go.Table(header=dict(values=["Concert","Date","Correct?"],fill=dict(color=("rgb(82,187,47)"))),cells=dict(values=[df_table.concert,df_table.date,df_table.correct],font=dict(color=([df_table.color]))))

data_table = [trace_table]

app.layout = html.Div(children=[
    html.Div(
        [
            dcc.Markdown(
                """
                ## My experience at Lollapalooza Brazil 2018
                For the 2018 edition of Lollapalooza Brazil all purchases were made through a RFID-enabled wristband. They sent the data of all purchases to our email addresses, so I decided to take a look at it. What can we learn about me and my experience by analyzing the purchases I did at the festival?
                ***
                """.replace('  ', ''),
                className='eight columns offset-by-two'
            )
        ],
        className='row',
        style=dict(textAlign="center",marginBottom="15px")
    ),

    html.Div([
        html.Div([
            html.H5('Where did I go?', style=dict(textAlign="center")),
            html.Div('Places where I bought food/beverage', style=dict(textAlign="center")),
            dcc.Graph(id='map', figure = figure_map),
            dcc.Markdown("""***""".replace('  ',''),className='eight columns offset-by-two')
        ], className="twelve columns"),
    ], className="row"),

     html.Div([
        html.Div([
            html.H5('How did I spend my money?'),
            dcc.Graph(id='g1', figure = figure_food_type) 
        ], className="five columns offset-by-one"),
    
        html.Div([
            html.H5('When did I spend?'),
            dcc.Graph(id='g2', figure = figure_heatmap)
        ], className="five columns offset-by-one"),
    ], className="row"),
 
    html.Div([html.Div([dcc.Markdown("""***""".replace('  ',''))], className="eight columns offset-by-two")], className="row"),

    html.Div([
        html.Div([
            html.H5('Which concerts have I attended?', style=dict(textAlign="center")),
            html.Div('People usually buy things before or after a concert, so I took the list of concerts, got the distances from the location of the purchases to the stages and tried to guess which concerts have I attended. 8 concerts were correct and 3 were missing from a total of 12 concerts.', style=dict(textAlign="center")),
            dcc.Graph(id='g6', figure=go.Figure(data=data_table,layout=go.Layout(margin=dict(t=30)))),
        ], className="twelve columns"),
    ], className="row")
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
