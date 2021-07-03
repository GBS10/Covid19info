import urllib
import branca
import folium
import pandas as pd
df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
df= df[(df.Date.isin(['2020-05-19']))]
m=folium.Map(location=[33.000000,65.000000],tiles='Stamen toner',zoom_start= 4 )
folium.Circle(location= [33.000000,65.000000],radius=10000, color='gold', fill=True,popup='{}Confirmed'.format(5)).add_to(m)
def circle_maker(x):
    folium.Circle(location= [x[0],x[1]],
                  radius=float(x[2]*10),
                  color='gold',
                  fill=True,
                  popup='{}\nConfirmed cases: {}'.format(x[3], x[2])).add_to(m)
df[['Lat','Long','Confirmed','Country/Region']].apply(lambda x: circle_maker(x),axis =1)
html_map=m._repr_html_()
from flask import Flask,render_template,request
import sys
app=Flask(__name__)
@app.route('/')
def livetracker():
    html_map=m._repr_html_()
    return render_template('index.html',cmap=html_map)
if __name__=="__main__":
	app.run(debug='True')
