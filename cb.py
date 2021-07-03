import nltk
from nltk.stem import WordNetLemmatizer
import numpy
from tensorflow.python.framework import ops
import tensorflow
import random
import json
import tflearn
import flask
import pickle
from flask import *
app=Flask(__name__)
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
@app.route("/")
def home():    
    return render_template("chatgui.html") 
if __name__=="__main__":
	app.run()
