import connector
from mongoengine import *
import datetime

class fireData(DynamicDocument):
	status = StringField()
	location = GeoPointField()
	NotifyTo = ListField(StringField())
	time = DateTimeField(default=datetime.datetime.now)

