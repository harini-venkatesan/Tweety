from elasticsearch import Elasticsearch, helpers
import requests, sys, json, os
from pprint import pprint
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['localhost'],
    port=9200

)

res = requests.get('http://localhost:9200')

MyFile= open("CS_data.json",'r').read()
ClearData = MyFile.splitlines(True)
i=0
json_str=""
docs ={}
for line in ClearData:
    line = ' '.join(line.split())
    for word in line:
        if word != "}":
                json_str = json_str+word
       

        else:
                docs[i]=json_str+"}"
                json_str=""
                es.index(index='tweets', doc_type='tweet', id=i, body=docs[i])
                i=i+1

print es.get(index='tweets', doc_type='tweet', id=0)
print es.search(index='tweets', q='California')

