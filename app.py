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

road_acc=[]
fire_acc=[]
cas_3=[]
cas_4=[]



@app.route('/',methods=['GET','POST'])
def get_tag():
	if request.method=='POST':
		file=request.files['file']
		image = Image.open(file)
	#	image.save('image.jpg',quality=30)
		image.save(os.path.join(app.config['UPLOAD_FOLDER'], "image.jpg"),quality=30)
		result = clarifai_api.tag_images(open('image.jpg'))
		tags = result["results"][0]["result"]["tag"]["classes"]
		fire = fireData()
		fire.tags=tags
		fire.location=None
		fire.save()
		return json.dumps(tags)
		
	else:
		return render_template('index.html')



port = int(os.environ.get('PORT', 5000))

app.run(host="0.0.0.0",port=port,debug=True)
