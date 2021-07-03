from flask import Flask, render_template,request
import pandas as pd
import plotly.express as pg
import folium
import urllib
import GetOldTweets3 as got3
import pickle
import tensorflow
import nltk
from nltk.stem import WordNetLemmatizer
import numpy
from tensorflow.python.framework import ops
import random
import json
import tflearn
import langid
from newsapi import NewsApiClient
app = Flask(__name__)
from translation import google,bing,ConnectError
from googletrans import Translator
vfnames=[]
vlnames=[]
vphones=[]
vemails=[]
vaddrs=[]
dfnames=[]
dlnames=[]
dphones=[]
demails=[]
dmoney=[]
val=0
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
translator = Translator()
lemmatizer = WordNetLemmatizer()
ignore_words=['?','.','!']
with open('intents.json') as file:
    data = json.load(file)
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
	words = []
	labels = []
	docs_x = []
	docs_y = []
	for intent in data['intents']:
		for pattern in intent['patterns']:
			wrds = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			docs_y.append(intent["tag"])
			if intent['tag'] not in labels:
				labels.append(intent['tag'])
	words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
	words = sorted(list(set(words)))
	labels = sorted(labels)
	training = []
	output = []
	out_empty = [0 for _ in range(len(labels))]
	for x, doc in enumerate(docs_x):
		bag = []
		wrds = [lemmatizer.lemmatize(w.lower()) for w in doc]
		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)
		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1
		training.append(bag)
		output.append(output_row)
	with open("data.pickle", "wb") as f:
		pickle.dump((words, labels, training, output), f)
tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)
try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
training = numpy.array(training)
output = numpy.array(output)
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)
@app.route('/get')
def get_bot_response():
    try:
        while True:
            inp = request.args.get('msg')    
            results = model.predict([bag_of_words(inp, words)])
            results_index = numpy.argmax(results)
            tag = labels[results_index]
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            if(random.choice(responses)=="See you later, thanks for visiting" or random.choice(responses)== "Have a nice day" or random.choice(responses)=="Bye! Come back again soon." or random.choice(responses)=="Its was nice to talk"):
                return(str(random.choice(responses))) 
                quit()
            else:
                return(str(random.choice(responses))) 
    except Exception as e:
	    return render_template("error.html", error = str(e))
@app.route('/')
def Index():
	try:
		newsapi = NewsApiClient(api_key="b0f75ce660c0466a9a98c2478f8abb62")
		topheadlines = newsapi.get_top_headlines(sources="the-times-of-india")
		articles = topheadlines['articles']
		desc = []
		news = []
		img = []
		for i in range(len(articles)):
			myarticles = articles[i]
			news.append(myarticles['title'])
			desc.append(myarticles['description'])
			img.append(myarticles['urlToImage'])
		mylist = zip(news, desc, img)
		mdu_c=corona_dist()
		corona_count = Corona_State()
		fig=graph_1().to_html()
		html_map=m._repr_html_()
		return render_template('index.html', context = mylist,table = mdu_c,map=corona_count,pair1=pair1,pair2=pair2,fig=fig,cmap=html_map)
	except Exception as e:
	    return render_template("error.html", error = str(e))
def Corona_State():
	coronadf=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
	coronadf.head()
	corona_count=coronadf.groupby('State').sum()[['Delta_Confirmed','Delta_Deaths','Delta_Recovered']]
	corona_count.head()
	pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]
	return corona_count
def corona_dist(): 
    corona2=pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
    corona2.head()
    mdu=corona2[corona2['District'].str.contains('Madurai')]
    mdu_c=mdu.groupby('District').sum()[['Confirmed','Recovered','Active']]
    mdu_c.head()
    return mdu_c 
def graph_1():
    df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
    df
    cdf=df[df['Country/Region'].str.contains('India')]
    cols=['Date','Confirmed']
    cdf1=cdf[cols]
    fig=pg.bar(cdf1,x='Date',y='Confirmed',title = 'Corona confirmation all across India : Time series')
    return fig
df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
df= df[(df.Date.isin(['2020-05-19']))]
m=folium.Map(location=[21.0,78.0],tiles='Stamen toner',zoom_start= 4 )
folium.Circle(location= [21.0,78.0],radius=100000, color='gold', fill=True,popup='{}Confirmed'.format("132000")).add_to(m)
def circle_maker(x):
    folium.Circle(location= [x[0],x[1]],
                  radius=float(x[2]*10),
                  color='gold', 
                  fill=True,
                  popup='{}\nConfirmed cases: {}'.format(x[3], x[2])).add_to(m)
df[['Lat','Long','Confirmed','Country/Region']].apply(lambda x: circle_maker(x),axis =1)
fig=graph_1()
mdu_c=corona_dist()
pair1=[(District,Confirmed,Recovered,Active) for District,Confirmed,Recovered,Active in zip(mdu_c.index,mdu_c['Confirmed'],mdu_c['Recovered'],mdu_c['Active'])]
corona_count = Corona_State()
pair2=[(State,Delta_Confirmed,Delta_Deaths,Delta_Recovered) for State,Delta_Confirmed,Delta_Deaths,Delta_Recovered in zip(corona_count.index,corona_count['Delta_Confirmed'],corona_count['Delta_Deaths'],corona_count['Delta_Recovered'])]
@app.route("/public")
def public():
    try:
        return render_template("font-awesome.html")
    except Exception as e:
	    return render_template("error.html", error = str(e))
@app.route("/donation",methods=["GET","POST"]) 
def donation():
	try:
		return render_template("basic_elements.html")
	except Exception as e:
		return render_template("error.html", error = str(e))
@app.route("/donate",methods=["GET","POST"])
def donate():
	if request.method=="POST":
		print("Here")
		pd=request.form
		Amount=pd['amt']
		payment=pd['pay']
		fname=pd['fname']
		lname=pd['lname']
		Mail=pd['email']
		phone=pd['phn']
		dfnames.append(fname)
		dlnames.append(lname)
		demails.append(Mail)
		dmoney.append(Amount)
		dphones.append(phone)
	return render_template('checkout.html',firstname=fname,lastname=lname,mail=Mail,phn=phone,amount=Amount,pm=payment)      
@app.route("/Thankyou",methods=["GET","POST"])
def thankyou():
    try:
        return render_template("volenteer.html")
    except Exception as e:
	    return render_template("error.html", error = str(e))
@app.route("/about",methods=["GET","POST"])
def about():
    try:
        return render_template("about.html")
    except Exception as e:
	    return render_template("error.html", error = str(e))
@app.route("/helpdesk")
def helpdesk():
    try:
        return render_template("helpdesk.html")
    except Exception as e:
	    return render_template("error.html", error = str(e))
@app.route('/tweets',methods=['POST','GET'])
def tweet_scrap():
    try:
        username1="Vijayabaskarofl"
        count=10
        username2="SuVe4Madurai"
        username3="narendramodi"
        tweetCriteria1=got3.manager.TweetCriteria().setUsername(username1).setMaxTweets(count)
        tweetCriteria2=got3.manager.TweetCriteria().setUsername(username2).setMaxTweets(count)
        tweetCriteria3=got3.manager.TweetCriteria().setUsername(username3).setMaxTweets(count)
        dict_obj_eng1=my_dictionary()
        dict_obj_tam1=my_dictionary()
        dict_obj_eng2=my_dictionary()
        dict_obj_tam2=my_dictionary()
        dict_obj_eng3=my_dictionary()
        dict_obj_tam3=my_dictionary()
        for i in range(count):
            tweets1=got3.manager.TweetManager.getTweets(tweetCriteria1)[i]
            result1=langid.classify(tweets1.text)
            try:		
                if(result1[0]=='en'):
                    dict_obj_eng1.add(str(tweets1.date),tweets1.text)
                    translated = translator.translate(tweets1.text,src='en',dest='ta')
                    dict_obj_tam1.add(str(tweets1.date),translated.text)
                elif(result1[0]=='ta'):
                    dict_obj_tam1.add(str(tweets1.date),tweets1.text)
                    translated = translator.translate(tweets1.text,src='ta',dest='en')
                    dict_obj_eng1.add(str(tweets1.date),translated.text)
            except:
                continue
        for i in range(count):
            tweets2=got3.manager.TweetManager.getTweets(tweetCriteria2)[i]
            result2=langid.classify(tweets2.text)
            try:
                if(result2[0]=='en'):
                    dict_obj_eng2.add(str(tweets2.date),tweets2.text)
                    translated = translator.translate(tweets2.text,src='en', dest='ta')
                    dict_obj_tam2.add(str(tweets2.date),translated.text)
                elif(result2[0]=='ta'):
                    dict_obj_tam2.add(str(tweets2.date),tweets2.text)
                    translated = translator.translate(tweets2.text,src='ta', dest='en')
                    dict_obj_eng2.add(str(tweets2.date),translated.text)
            except:
                continue
        for i in range(count):
            tweets3=got3.manager.TweetManager.getTweets(tweetCriteria3)[i]
            result3=langid.classify(tweets3.text)
            try:
                if(result3[0]=='en'):
                    dict_obj_eng3.add(str(tweets3.date),tweets3.text)
                    translated = translator.translate(tweets3.text,src='en', dest='ta')
                    dict_obj_tam3.add(str(tweets3.date),translated.text)
                elif(result3[0]=='hi'):
                    translatedt= translator.translate(tweets3.text,src='hi', dest='ta')
                    dict_obj_tam3.add(str(tweets3.date),translatedt.text)
                    translated = translator.translate(tweets3.text,src='hi', dest='en')
                    dict_obj_eng3.add(str(tweets3.date),translated.text)
            except:
                continue
        return render_template('tweet.html',dict_obj_eng1=dict_obj_eng1,dict_obj_eng2=dict_obj_eng2,dict_obj_eng3=dict_obj_eng3,dict_obj_tam1=dict_obj_tam1,dict_obj_tam2=dict_obj_tam2,dict_obj_tam3=dict_obj_tam3)
    except Exception as e:
	    return render_template("error.html", error = str(e))
if __name__ == "__main__":
    app.run(debug=True) 