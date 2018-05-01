import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
 
app = dash.Dash()

df_table = pd.read_csv("data/concerts_I_attended.csv").dropna(subset=["concert"])

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
            html.H5('Which concerts did I attend?', style=dict(textAlign="center")),
            html.Div('People usually buy things before or after a concert, so I took the list of concerts, got the distances from the location of the purchases to the stages and tried to guess which concerts did I attend. 8 concerts were correct and 3 were missing from a total of 12 concerts.', style=dict(textAlign="center")),
            dcc.Graph(id='g6', figure=go.Figure(data=data_table,layout=go.Layout(margin=dict(t=30)))),
        ], className="twelve columns"),
    ], className="row")
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
