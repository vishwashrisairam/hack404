import connector
from mongoengine import *
import datetime

class fireData(DynamicDocument):
	status = StringField()
	location = GeoPointField()
	NotifyTo = StringField()
	time = DateTimeField(default=datetime.datetime.now)

