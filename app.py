from flask import Flask,request,render_template
from clarifai.client import ClarifaiApi
import os
import json
import connector
from model import *
from PIL import Image

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

clarifai_api = ClarifaiApi("Chxllj0Bp9NVtfTBqZcYXOgrjvLiSrvi81NbhF5E","xA0eLr_QoIU39Z00VM5yrf_xSB__iTVEoDKz_eTL")

#tags for different cassualties
road_acc=["accident","crash","calamity","road","isolated"]
fire_acc=["flame","smoke","danger","heat","burn"]
cas_3=[]
cas_4=[]


@app.route('/',methods=['GET','POST'])
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
				#fire.tags=tags
				fire.location=None
				fire.save()
				print(fire)
			elif bool(set(fire_acc) & set(tags)):
				fire = fireData()
				fire.status="fire"
				#fire.tags=tags
				fire.location=None
				fire.save()
				print(fire)
			elif bool(set(cas_3) & set(tags)):
				fire = fireData()
				fire.status="casualty3"
				#fire.tags=tags
				fire.location=None
				fire.save()	
				print(fire)
			else: 
				print("NO match")			
			return json.dumps(tags)

		except Exception as e:
				dict = {}
				dict["msg"] = str(e)
				return json.dumps(dict)
	else:
		return render_template('index.html')
		# dict=[]
		# for fd in fireData.objects():
		# 	local={}
		# 	for keys in fd:
		# 		local[keys]=str(fd[keys])
		# 	dict.append(local)
		# return render_template("dashboard.html",data=dict)		
		


port = int(os.environ.get('PORT', 5000))

app.run(host="0.0.0.0",port=port,debug=True)
