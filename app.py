import requests
import json
import pymongo

#get foreign exchange data from exchangeratesapi.io using their public api
resp = (requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=f27c66a897df264865447f0c2c682894"))


# https://appdividend.com/2020/11/20/how-to-convert-python-string-to-dictionary/
# conv_data = json.loads(resp.text)
# rates = conv_data['rates']
# print(str(rates))

# ref mongodb documentation

#ERROR
# raise ConfigurationError(
# pymongo.errors.ConfigurationError: The "dnspython" module must be installed to use mongodb+srv:// URIs. To fix this error install pymongo with the srv extra: 
#  D:\INSTALL\PYTHON\310\python.exe -m pip install "pymongo[srv]"
#ERROR

#conn string for mongoCompass 'mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/test'

client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
