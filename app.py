from pymongo import database
import requests
import json
import pymongo
from datetime import datetime
import time
import smtplib

# REF Send email
# 1) https://docs.python.org/3/library/smtplib.html
# 2) https://realpython.com/python-send-email/#sending-a-plain-text-email
# 3) https://zetcode.com/python/smtplib/

def sendEmail(receiverMailID : str):
    senderMailID = "10585724.dbs@gmail.com"
    password = "YeavNnxO19U"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp: #use port 587 for gmail
        # print(1)
            smtp.starttls()
        # print(2)
            smtp.login(senderMailID, password)
        # print(3)
            subject = "Hey there"
            body = "Hi!"

            mail = "Subject : " + subject + "\n\n" + body
            print(mail)

            smtp.sendmail(senderMailID, receiverMailID, mail)

    except smtplib.SMTPException as e:
        print(1)
        print(str(e))

    except Exception as e:
        print(2)
        print(str(e))

# test sendEmail("mashhuda20297@gmail.com")

while(True):
    try:

        #get foreign exchange data from exchangeratesapi.io using their public api
        resp = (requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=f27c66a897df264865447f0c2c682894"))

        #REF convert text to dictionary https://appdividend.com/2020/11/20/how-to-convert-python-string-to-dictionary/
        conv_data = json.loads(resp.text)

        rates = conv_data['rates'] #{'AED': 4.134561, 'AFN': 115.381694, 'ALL': 120.117061, 'AMD': 540.984044, ...}
        # print(str(rates)) #TEST DATA HERE

        #conn string for mongoCompass 'mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/test'

        # REF mongodb documentation for connection with python :
        # 1) https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/
        # 2) https://docs.mongodb.com/drivers/python/

        client = pymongo.MongoClient("mongodb+srv://siddhant:b9cy-ca2@b9cyca2-database.oqc5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        
        #ERROR + ERROR FIX
        # raise ConfigurationError(
        # pymongo.errors.ConfigurationError: The "dnspython" module must be installed to use mongodb+srv:// URIs. To fix this error install pymongo with the srv extra: 
        #  D:\INSTALL\PYTHON\310\python.exe -m pip install "pymongo[srv]"
        #ERROR

        database = client["ca2db"]

        exchangeRates = database["exchangeRates"]
        userSubs = database["userSubs"]

        rateCollection = []

        #TRANSFORM DATA INTO BELOW FORMAT FOR INSERTING INTO COLLECTION:
        #TARGET FORMAT - [{"currency" : "AED", "value" : 4.134561}, {...}, {...}]
        #CURRENT FORMAT RECVD. FROM RESPONSE- {'AED': 4.134561, 'AFN': 115.381694, 'ALL': 120.117061, 'AMD': 540.984044, ...}
        
        for k, v in rates.items():
            dictObject = {"currency" : k, "value" : v}
            rateCollection.append(dictObject)
        # print(str(rateCollection))

        # REF pymongo documentation https://pymongo.readthedocs.io/en/stable/genindex.html

        #remove existing records
        exchangeRates.delete_many({}) #perform delete operation before insertion to prevent duplication

        #insert fresh exchange rates
        exchangeRates.insert_many(rateCollection)
        #ERROR & FIX : occured error while insertion [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:997)')
        #REF solution to insertion error : https://www.mongodb.com/community/forums/t/keep-getting-serverselectiontimeouterror/126190/7

        # data = database.exchangeRates.find({}, {"_id" : 0}) #get data without "_id" property
        # print(str(data)) #<pymongo.cursor.Cursor object at 0x000002685EA60340> data unreadable

        # for item in data:
        #     print(str(item))

        #REF https://zetcode.com/python/pymongo/
        # print(list(data))

        userData = userSubs.find({}, {"_id" : 0})

        #iterate through saved user data

        for user in userData:
            print(str(user))

        print (datetime.now())

        time.sleep(43200) #fetch new data and update every 12 hrs

    except Exception as e:
        with open("errors.txt", "a") as err:
            err.write("\n Error : " + str(e) + "/ Timestamp : " + str(datetime.now()))
        
        continue