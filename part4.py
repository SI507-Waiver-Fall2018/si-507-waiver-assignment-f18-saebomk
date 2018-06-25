# Saebom Kwon, saebom, 38120092, SI507 Waiver

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.figure_factory as FF

plotly.tools.set_credentials_file(username='aprilsbkwon', api_key='zF3R7DO5fzj3XRbz3Z1u')

df = pd.read_csv('noun_data.csv')
sample_data_table = FF.create_table(df.head())
py.iplot(sample_data_table, filename='sample-data-table')

trace = go.Bar(x= df['Noun'], y= df['Number'])
data = [trace]
layout = go.Layout(title='Twitter Word Frequency', width=800, height=640)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='part4_viz_image.png')
