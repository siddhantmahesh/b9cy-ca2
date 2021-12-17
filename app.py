import requests
import json

#get foreign exchange data from exchangeratesapi.io using their public api
resp = (requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=f27c66a897df264865447f0c2c682894"))


# https://appdividend.com/2020/11/20/how-to-convert-python-string-to-dictionary/
conv_data = json.loads(resp.text)
rates = conv_data['rates']
print(str(rates))

