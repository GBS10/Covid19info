import json
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
from chart_studio.plotly import iplot
with open('raw_data.json') as file:
    data = json.load(file)
ages = [i['agebracket'] for i in data["raw_data"]]
gender = [i['gender'] for i in data['raw_data']]
# prepare data frames
# import graph objects as "go"
import plotly.graph_objs as go
# creating trace1
trace1 =go.Scatter(
                    x = ages,
                    y = gender,
                    mode = "markers",
                    name = "2014",
                    marker = dict(color = 'rgba(255, 128, 255, 0.8)'),
                    text="blah")
# creating trace2
data = [trace1]
layout = dict(title = 'Citation vs world rank of top 100 universities with 2014, 2015 and 2016 years',
              xaxis= dict(title= 'World Rank',ticklen= 5,zeroline= False),
              yaxis= dict(title= 'Citation',ticklen= 5,zeroline= False)
             )
fig = dict(data = data, layout = layout)
iplot(fig)