from flask import Flask, request
import pymongo
from datetime import datetime
from flask_cors import CORS
from pymongo.collection import ReturnDocument

# REF https://flask-cors.readthedocs.io/en/latest/
app = Flask(__name__)
CORS(app) # ENABLE CROSS ORIGIN REQUESTS
app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["ca2db"] #db instance
exchangeRates = database["exchangeRates"] #rates collection instance
userSubs = database["userSubs"] #subs collection instance

# REF https://flask.palletsprojects.com/en/2.0.x/quickstart/

@app.route('/getRates')
def getRates ():
    try:
        data = database.exchangeRates.find({}, {"_id" : 0}) #select from collection, _id not required for UI
        resultData = {}

        for item in list(data):
            resultData[item["currency"]] = item["value"] #transform data for front end suitability

        return {
            "code" : 200, #200 for success
            "msg" : "Success",
            "rates" : resultData
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/getRates')/Timestamp : " + str(datetime.now())) #log any errors

        return {
            "code" : 500, #500 for error
            "msg" : str(e),
            "rates" : ""
        }
        
@app.route('/getUser/<email>')
def getUser (email):
    try:
        result = database.userSubs.find({"email" : email}) #find document where "email" = email
        resultData = list(result)

        #RESPONSE
        return {
            "code" : 200,
            "msg" : "Success",
            "data" : resultData
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/getUser/<email>')/Timestamp : " + str(datetime.now()))

        return {
            "code" : 500,
            "msg" : str(e),
            "data" : ""
        }

@app.route('/addUser', methods=['POST']) #add new user data
def addUser ():
    try:
        data = request.get_json()
        # SAMPLE DATA {
        #   "email" : "abc@abc", DONOT ADD DISPARATE EMAIL ADDRESS, BREAKS SEND EMAIL CODE IN APP.PY
        #   "name" : "jon paul",
        #   "currency" : "USD",
        #   "threshold" : 1.13, 
        #   "condition" : False (True == ABOVE; False == BELOW)
        # }
        if(userSubs.count_documents({"email" : data["email"]}) > 0) :
            return {
                "code" : 500,
                "msg" : "Success",
                "data" : "Already Exists"
            }
        else :
            resultData = userSubs.insert_one(data).inserted_id

            #RESPONSE
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
            "data" : ""
        }

# REF https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
@app.route('/updateUser', methods=['POST']) #updating existing user data
def updateUser ():
    try:
        data = dict(request.get_json())
        # print (str(data))

        # print(list(userSubs.find({"_id" : ObjectId(data["_id"])})))
        result = userSubs.find_one_and_update({'email' : data["email"]}, #update below fields where "email" = email
            {
                '$set' : {
                            "name" : data["name"],
                            "currency" : data["currency"],
                            "threshold" : data["threshold"],
                            "condition" : data["condition"]
                        }
            }, 
            return_document=ReturnDocument.AFTER) #return updated document after insertion

        # print (1)
        # print(str(result))
        # resultData = list(result)

        #RESPONSE
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
            "data" : ""
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080') #add debug=true for dev purpose