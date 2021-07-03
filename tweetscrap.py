import GetOldTweets3 as got3
from flask import *
from flask import request
import langid
app=Flask(__name__)
from translation import google,bing,ConnectError
from googletrans import Translator
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
translator = Translator()
@app.route('/',methods=['POST','GET'])
def tweet_scrap():
	username1="Vijayabaskarofl"
	count=20
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
				translated = translator.translate(tweets2.text,src='en', dest='ta')
				dict_obj_tam3.add(str(tweets3.date),translated.text)
			elif(result3[0]=='hi'):
				translatedt= translator.translate(tweets3.text,src='hi', dest='ta')
				dict_obj_tam3.add(str(tweets3.date),translatedt.text)
				translated = translator.translate(tweets2.text,src='hi', dest='en')
				dict_obj_eng3.add(str(tweets3.date),translated.text)
		except:
			continue
	return render_template('tweets.html',dict_obj_eng1=dict_obj_eng1,dict_obj_eng2=dict_obj_eng2,dict_obj_eng3=dict_obj_eng3,dict_obj_tam1=dict_obj_tam1,dict_obj_tam2=dict_obj_tam2,dict_obj_tam3=dict_obj_tam3)
if __name__=='__main__':
	app.run()

