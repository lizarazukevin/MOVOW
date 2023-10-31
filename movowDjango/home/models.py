from django.db import models
#from movowDjango import mongo_connection
import pymongo

key = "mongodb+srv://jasperemick:lB7P6QQdJtrox4k9@movow1.yk4hwgi.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(key)

db = client['movow1']
# Create your models here.

movie_collection = db['movies']

