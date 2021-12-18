from flask import Flask, request
import pymongo
import requests

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["ca2db"] #db instance
exchangeRates = database["exchangeRates"] #collection instance

# REF https://flask.palletsprojects.com/en/2.0.x/quickstart/

@app.route('/getRates')
def getRates ():

    data = database.exchangeRates.find({}, {"_id" : 0}) #select from collection
    listData = []

    for item in list(data):
        listData.append({item["currency"] : item["value"]}) #transform data for front end suitability

    return str(listData) #return as string/dict DOESNT return as list

@app.route('/addUser', methods=['POST']) #add new user data
def insertNewUser ():

    data = request.get_json()
    return str(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080',debug=True) #add debug=true for dev purpose