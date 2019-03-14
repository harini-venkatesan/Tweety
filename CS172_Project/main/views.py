from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
import json, re

connections.create_connection()
# Create your views here.
def homepage(request):
    return render(request = request, template_name = "main/home.html")

def search_tweet(request):
    template = 'main/search.html'
    es = Elasticsearch(['localhost'],port=9200)
    if 'q' in request.GET:
        query = request.GET['q']
        res = es.search(index="tweets", q=query, size=100)
    results = []
    url = ''
    for hit in res['hits']['hits']:
        dic = hit["_source"]
        dic['hash_tags'] = ''.join(dic['hash_tags'])
        # parse tweet_text to extract urls
        # Needs refinement: if tweet text contains
        #       more than 1 url assigns the last url
        #       to all places where url was found
        # Original: You're So Pretty – We're So Pretty - The Charlatans (Wonderland - 2001) https://t.co/A1QMEV05FW #TimBurgess https://t.co/ObbJO7wmST
        # Results: You're So Pretty – We're So Pretty - The Charlatans (Wonderland - 2001) https://t.co/ObbJO7wmST #TimBurgess https://t.co/ObbJO7wmST
        text = dic['tweet_text']
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        for  link in url:
            dic['tweet_text'] = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'<a href="'+link+'"> '+link+' </a> ', text)
        results.append(hit["_source"])
    
    context = {'results': results, 'query': query}
    return render(request, template, context)
#TODO
def near_me(request):
    return render(request, template_name = "main/near.html")

def world_wide(request):
    return render(request, template_name = "main/worldwide.html")

def most_recent(request):
    return render(request, template_name = "main/recent.html")