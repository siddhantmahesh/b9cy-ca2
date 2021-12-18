from bson.objectid import ObjectId
from flask import Flask, request
import pymongo
from datetime import datetime

from pymongo.collection import ReturnDocument

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["ca2db"] #db instance
exchangeRates = database["exchangeRates"] #rates collection instance
userSubs = database["userSubs"] #subs collection instance

# REF https://flask.palletsprojects.com/en/2.0.x/quickstart/

@app.route('/getRates')
def getRates ():
    try:
        data = database.exchangeRates.find({}, {"_id" : 0}) #select from collection
        resultData = []

        for item in list(data):
            resultData.append({item["currency"] : item["value"]}) #transform data for front end suitability

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(resultData) #return as string/dict DOESNT return as list
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/getRates')/Timestamp : " + str(datetime.now()))

        return {
            "code" : 500,
            "msg" : str(e),
            "data" : [] #return as string/dict DOESNT return as list
        }
        
@app.route('/getUser/<email>')
def getUser (email):
    try:
        result = database.userSubs.find({"email" : email})
        resultData = list(result)

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(resultData)
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/getUser/<email>')/Timestamp : " + str(datetime.now()))

        return {
            "code" : 500,
            "msg" : str(e),
            "data" : []
        }

@app.route('/addUser', methods=['POST']) #add new user data
def addUser ():
    try:
        data = request.get_json()
        # SAMPLE DATA {
        #   "email" : "abc@abc",
        #   "name" : "jon paul",
        #   "currency" : "USD",
        #   "threshold" : 1.13, 
        #   "condition" : False (True == ABOVE; False == BELOW)
        # }
        result = userSubs.insert_one(data)
        resultData = list(result)

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(resultData)
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/addUser', methods=['POST'])/Timestamp : " + str(datetime.now()))
        
        return {
            "code" : 500,
            "msg" : str(e),
            "data" : []
        }

# REF https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
@app.route('/updateUser', methods=['POST']) #add new user data
def updateUser ():
    try:
        data = dict(request.get_json())
        # print (str(data))

        # print(list(userSubs.find({"_id" : ObjectId(data["_id"])})))
        result = userSubs.find_one_and_update({'email' : data["email"]},
            {
                '$set' : {
                            "name" : data["name"],
                            "currency" : data["currency"],
                            "threshold" : data["threshold"],
                            "condition" : data["condition"]
                        }
            }, 
            return_document=ReturnDocument.AFTER)

        # print (1)
        # print(str(result))
        # resultData = list(result)

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(result)
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/updateUser', methods=['POST'])/Timestamp : " + str(datetime.now()))
        
        return {
            "code" : 500,
            "msg" : str(e),
            "data" : []
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080',debug=True) #add debug=true for dev purpose