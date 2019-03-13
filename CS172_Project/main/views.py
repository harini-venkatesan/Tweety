from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

# Create your views here.
def homepage(request):
    return render(request = request, template_name = "main/home.html")

def search(request):
    # connect to elastic search here
    # create request
    # decode request
    # render it to HTML
    template = 'main/search.html'
    es = Elasticsearch()
    with open('CS_data.json', 'r') as f:
        def gen():
            for line in f:
                yield {
                    "_index": "tweet-index",
                    "_type": "doc",
                    "doc": {"word": line},
                }
        bulk(es, gen())
    if 'q' in request.GET:
        query = request.GET['q']
        res = es.search(index="tweet-index", q=query)
    results = []
    for hit in res['hits']['hits']:
        results.append(json.loads(hit["_source"]['doc']['word']))
    context = {'results': results, 'query': query}
    return render(request, template, context)