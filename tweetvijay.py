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
def vtweet_scrap():
	username1="Vijayabaskarofl"
	count=30

	tweetCriteria1=got3.manager.TweetCriteria().setUsername(username1).setMaxTweets(count)
	
	dict_obj_eng1=my_dictionary()
	dict_obj_tam1=my_dictionary()

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
	return render_template('tweets.html',dict_obj_eng1=dict_obj_eng1,dict_obj_tam1=dict_obj_tam1)
if __name__=='__main__':
	app.run()

