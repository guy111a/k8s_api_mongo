
import pymongo
import time
import random


mongo_host = '10.0.0.21'
mDB = ''
mCollection = ''

myclient = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")

mydb = myclient[f"mDB"]
mycol = mydb[f"mCollection"]

rNum = random.randrange(1,10)

collection = { "timestamp" : int(time.time()), "randomNumber" : rNum }

res = mycol.insert_one(collection)

print(res)
