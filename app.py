from flask import Flask,request,render_template
from clarifai.client import ClarifaiApi
import os
import json
import connector
from model import *
from PIL import Image


from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC6b6c7686e9c8f2be3a1c3d8aa09e2206" 
AUTH_TOKEN = "9a8072af69a8a13fd93094a22f1668c7" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
# client.messages.create( 
# 	from_="+14243243409",
# 	to_="+91"   
# )

 

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

clarifai_api = ClarifaiApi("Chxllj0Bp9NVtfTBqZcYXOgrjvLiSrvi81NbhF5E","xA0eLr_QoIU39Z00VM5yrf_xSB__iTVEoDKz_eTL")

#tags for different cassualties
road_acc=["accident","crash","calamity","road","isolated"]
fire_acc=["flame","smoke","danger","heat","burn"]
cas_3=["protest","rally","battle","rebelion"]
cas_4=[]

@app.route('/test',methods=['GET'])
def test():
	return render_template("index.html")

@app.route('/')
def index():
	return render_template("1.html")


@app.route('/dash',methods=['GET','POST'])
def get_tag():
	if request.method=='POST':
		try:
			file=request.files['file']
			image = Image.open(file)
	#		image.save('image.jpg')
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], "image.jpg"),quality=30)
			result = clarifai_api.tag_images(open(os.path.join(app.config['UPLOAD_FOLDER'],'image.jpg')))
			tags = result["results"][0]["result"]["tag"]["classes"]
			if bool(set(road_acc) & set(tags)):
				fire = fireData()
				fire.status="road"
				fire.NotifyTo=["ambulance","police"]
				fire.location=None
				fire.save()
				message = client.messages.create(body="Emergency: Road Accident at Location (41.42,-71.34) .Dispatch immediately",to="+918264578005",from_="+14243243409") 
				print message.sid

				print(fire)
			elif bool(set(fire_acc) & set(tags)):
				fire = fireData()
				fire.status="fire"
				fire.NotifyTo=["fire brigade","ambulance"]
				fire.location=None
				fire.save()
				message = client.messages.create(body="Emergency:Fire Breakout  at Location (41.42,-71.34) .Dispatch immediately",to="+918264578005",from_="+14243243409") 
				print message.sid
				print(fire)
			elif bool(set(cas_3) & set(tags)):
				fire = fireData()
				fire.status="casualty3"
				fire.NotifyTo=["police","army"]
				fire.location=None
				fire.save()	
				message = client.messages.create(body="Emergency: Cassualty at Location (41.42,-71.34) .Dispatch immediately",to="+918264578005",from_="+14243243409") 
				print message.sid
				print(fire)
			else: 
				print("NO match")			
			return json.dumps(tags)

		except Exception as e:
				dict = {}
				dict["msg"] = str(e)
				return json.dumps(dict)
	else:
		# return render_template('index.html')
		dict=[]
		for fd in fireData.objects():
			local={}
			for keys in fd:
				local[keys]=str(fd[keys])
			dict.append(local)
		return render_template("dashboard.html",data=dict)

@app.route('/delete',methods=['POST'])
def delete():
	id=request.form['id']
	fd=fireData.objects(id=id)
	fd[0].delete()
	return render_template("http://fireacc.herokusapp.com/")

@app.route('/filter',methods=['POST'])	
def filter():
	issue=request.form['is'];
	fd=fireData.objects(status=issue)
	dict=[]
	for f in fd:
		temp={}
		for keys in f:
			temp[keys]=str(f[keys])
		dict.append(temp)
	return render_template("dashboard.html",data=dict)			


port = int(os.environ.get('PORT', 5000))

app.run(host="0.0.0.0",port=port,debug=True)
