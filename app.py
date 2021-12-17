from pymongo import database
import requests
import json
import pymongo
from datetime import datetime


try:

    #get foreign exchange data from exchangeratesapi.io using their public api
    resp = (requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=f27c66a897df264865447f0c2c682894"))


    #REF convert text to dictionary https://appdividend.com/2020/11/20/how-to-convert-python-string-to-dictionary/
    conv_data = json.loads(resp.text)
    rates = conv_data['rates'] #{'AED': 4.134561, 'AFN': 115.381694, 'ALL': 120.117061, 'AMD': 540.984044, ...}
    # print(str(rates)) #TEST DATA HERE


    #ERROR + ERROR FIX
    # raise ConfigurationError(
    # pymongo.errors.ConfigurationError: The "dnspython" module must be installed to use mongodb+srv:// URIs. To fix this error install pymongo with the srv extra: 
    #  D:\INSTALL\PYTHON\310\python.exe -m pip install "pymongo[srv]"
    #ERROR

    #conn string for mongoCompass 'mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/test'


    # REF mongodb documentation for connection with python https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/
    # https://docs.mongodb.com/drivers/python/
    # REF pymongo documentation https://pymongo.readthedocs.io/en/stable/genindex.html

    client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    database = client["ca2db"]

    exchangeRates = database["exchangeRates"]

    #TRANSFORM DATA INTO BELOW FORMAT FOR INSERTING INTO COLLECTION:
    #TARGET FORMAT - [{"currency" : "AED", "value" : 4.134561}, {...}, {...}]
    #CURRENT FORMAT RECVD. FROM RESPONSE- {'AED': 4.134561, 'AFN': 115.381694, 'ALL': 120.117061, 'AMD': 540.984044, ...}

    rateCollection = []

    for k, v in rates.items():
        dictObject = {"currency" : k, "value" : v}
        rateCollection.append(dictObject)

    # print(str(rateCollection))

    #remove existing records
    exchangeRates.delete_many({}) #perform delete operation before insertion to prevent duplication

    #insert fresh exchange rates
    exchangeRates.insert_many(rateCollection)
    #occured error while insertion [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:997)')
    #REF solution to insertion error : https://www.mongodb.com/community/forums/t/keep-getting-serverselectiontimeouterror/126190/7

    data = database.exchangeRates.find({}, {"_id" : 0}) #get data without "_id" property
    # print(str(data)) #<pymongo.cursor.Cursor object at 0x000002685EA60340> data unreadable

    # for item in data:
    #     print(str(item))

    #REF https://zetcode.com/python/pymongo/
    print(list(data))
    
    print (datetime.now())
    
except Exception as e:
    with open("errors.txt", "a") as err:
        err.write("\n Error : " + str(e) + "/ Timestamp : " + str(datetime.now()))