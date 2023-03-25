
'''

REST API 
purpose:
    access mongoDB in closed network
usage:
    /listdbs => list dbs
    /search  => search in a DB and in a COLLECTION ( coma seperated )
            options:
                        db      : name of db
                        col     : name of collection
                        lim     : limit the results : to do
                        sort    : sort the results : to do 
    /deldb  => delete db
    /delcol => delete collection
    /add    => add record(s) to a DB and COLLECTION ( coma seperated )


'''
from flask import Flask, request, jsonify
import pymongo
import time

mongo_host = '10.0.0.21'

myclient = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")
dbs = myclient.list_database_names()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return 'ok\n'

@app.route("/listdbs", methods=['GET', 'POST'])
def listdb():
    return dbs

@app.route("/search", methods=['GET', 'POST'])
# curl "10.0.0.28:6666/search?db=12&col=ww&data=b,a&lim=2"
def search1():
    if 'db' in request.args:
        if 'col' in request.args:
            if 'data' in request.args:
                temp = []
                data = request.args['data'].split(",")
                for d in data:
                    new = (d, '1')
                    temp.append(new)
            else:
                temp = ''
            db = request.args['db']
            mydb = myclient[db]
            collection = request.args['col']
            mycol = mydb[collection]
            res = mycol.find({}, dict(temp))
            if res:
                t = []
                for r in res:
                    t.append(r)
            return f"{t}\n"
        else:
            return "missing Collection"
        # else:
        #     return 'missing DATA\n'
    else:
        return "missing DB\n"


@app.route("/deldb", methods=['GET', 'POST'])
def dropDB():
    if 'db' in request.args:
            db = request.args['db']
            mydb = myclient[db]
            mydb.dropDatabase()
            return f"Collection {mydb}, deleted\n"
    else:
        return "missing DB\n"
    
    
@app.route("/delcol", methods=['GET', 'POST'])
def dropCOL():
    if 'db' in request.args:
        if 'col' in request.args:
            db = request.args['db']
            collection = request.args['col']
            mydb = myclient[db]
            mycol = mydb[collection]
            mycol.drop()
            return f"Collection {collection}, deleted\n"
        else:
            return "missing COLLECTION\n"
    else:
        return "missing DB\n"
    
@app.route("/add", methods=['GET', 'POST'])
# curl "10.0.0.28:6666/add?db=12&col=ww&data=a=1,b=2,sdf=233,ggg=555"
def add1():
    if 'db' in request.args:
        if 'data' in request.args:
            if 'col' in request.args:
                temp = []
                db = request.args['db']
                collection = request.args['col']
                data = request.args['data'].split(",")
                temp.append(('timestamp', int(time.time())))
                for d in data:
                    x, y = d.split("=")
                    newD = (x, y)
                    temp.append(newD)
                mydb = myclient[db]
                mycol = mydb[collection]
                res = mycol.insert_one(dict(temp))
                return f"{res} : DB {db}, Col {collection}, DATA {dict(temp)}\n"
            else:
                return "missing Collection"
        else:
            return 'missing DATA\n'
    else:
        return "missing DB\n"

if __name__ == "__main__":
    app.run(debug=True, port='6666', host='0.0.0.0')

