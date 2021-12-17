from pymongo import database
import requests
import json
import pymongo

#get foreign exchange data from exchangeratesapi.io using their public api
resp = (requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=f27c66a897df264865447f0c2c682894"))


#convert text to dictionary https://appdividend.com/2020/11/20/how-to-convert-python-string-to-dictionary/
conv_data = json.loads(resp.text)
rates = conv_data['rates'] #{'AED': 4.134561, 'AFN': 115.381694, 'ALL': 120.117061, 'AMD': 540.984044, ...}
# print(str(rates)) #TEST DATA HERE


#ERROR
# raise ConfigurationError(
# pymongo.errors.ConfigurationError: The "dnspython" module must be installed to use mongodb+srv:// URIs. To fix this error install pymongo with the srv extra: 
#  D:\INSTALL\PYTHON\310\python.exe -m pip install "pymongo[srv]"
#ERROR

#conn string for mongoCompass 'mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/test'


# ref mongodb documentation for connection with python

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

print(str(rateCollection))

#occured error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:997)')
exchangeRates.insert_many(rateCollection)

print(str(exchangeRates.find()))
