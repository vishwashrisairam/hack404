import connector
from mongoengine import *
import datetime

class fireData(DynamicDocument):
	tags = ListField(StringField())
	location = GeoPointField()
	NotifyTo = StringField()
	time = DateTimeField(default=datetime.datetime.now)

