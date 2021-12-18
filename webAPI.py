from flask import Flask, request
import pymongo
import datetime

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
        listData = []

        for item in list(data):
            listData.append({item["currency"] : item["value"]}) #transform data for front end suitability

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(listData) #return as string/dict DOESNT return as list
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
        data = list(result)

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(data)
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
        data = list(result)

        return {
            "code" : 200,
            "msg" : "Success",
            "data" : str(data)
        }

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/@app.route('/addUser', methods=['POST'])/Timestamp : " + str(datetime.now()))
        
        return {
            "code" : 500,
            "msg" : str(e),
            "data" : []
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080',debug=True) #add debug=true for dev purpose