
import pymongo

mongo_host = '10.0.0.21'
mDB = ''
mCollection = ''

myclient = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")


mydb = myclient[f"mDB"]
mycol = mydb[f"mCollection"]


print(mydb.list_collection_names())
