from mongoengine import connect

connect("fireacc",host="mongodb://harsh:vadajasd@ds023428.mlab.com:23428/fireacc")
print "successfully connected to mongo"
