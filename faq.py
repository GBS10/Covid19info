#-------FaQ's-------
import flask
import re
app=Flask(__name__)
patterns={"spread","symptoms","cure","protect","prevent","pet","schools","colleges","cleaning and disinfection","travel","normal","self care"}
@app.route('/',methods=['POST','GET']):
def display_faq(**nthng):
	count=0
	uquery=request.form('uq')
	for pattern in patterns:
		if re.search(pattern,uquery):
			count=count+1
			return render_template("faq.html")
	if(count==0):
		return render_template('faqnotfound.html')