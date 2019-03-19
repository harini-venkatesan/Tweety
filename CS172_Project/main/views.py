from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
import json, re, string, xlrd
from textblob import TextBlob
import folium # for map

connections.create_connection()
# Create your views here.
def homepage(request):
    return render(request = request, template_name = "main/home.html")

def search_tweet(request):
    template = 'main/search.html' 
    # connect to elasticsearch
    es = Elasticsearch(['localhost'],port=9200)
    # check query
    if 'q' in request.GET:
        query = request.GET['q']
        # search for query in elasticsearch index
        res = es.search(index="tweet-index", q = query, size=100)
        results = []
        # paser the list of results returned by elasticsearch
        for hit in res['hits']['hits']:
            dic = hit["_source"] #get dictionary
            dic['hash_tags'] = ''.join(dic['hash_tags']) # remove [] from tag
            dic['score'] = hit['_score'] # get search result ranking
            # parse tweet_text to extract urls
            dic['tweet_text'] = re.sub(r'http[s]?://(?:[a-zA-Z]|0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                lambda x: r'<a href="'+ re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                x.group())[0] + '"> ' + re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                x.group())[0] + '</a> ', dic['tweet_text'])
            # add object to results list
            results.append(hit["_source"])

        context = {'results': results, 'query': query}
        return render(request=request, template_name=template, context=context)
    else:
        return render(request=request, template_name=template)

def world_wide(request):
    template = "main/worldwide.html"
    # connect to elasticsearch
    es = Elasticsearch(['localhost'],port=9200)
    # Open xlsx file
    loc = ("worldcities.xlsx") 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 

    m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=3)
    # check query
    if 'q' in request.GET:
        query = request.GET['q']
        # search for query in elasticsearch index
        res = es.search(index="tweet-index", q = query, size=1000)
        # paser the list of results returned by elasticsearch
        for hit in res['hits']['hits']:
            dic = hit["_source"] #get dictionary
            if dic['Location'] != None:
                location = dic['Location']
                clear_location = location.split()
                for row_num in range(sheet.nrows):
                        row_value = sheet.row_values(row_num)
                        if row_value[1] == clear_location[0]:
                                lat = row_value[2]
                                lon = row_value[3]
                                tweet_text = dic['tweet_text']
                                username = dic['user_name']
                                folium.Marker([lat, lon], "%s: %s "%(tweet_text,username)).add_to(m)
    context = {'m': m._repr_html_()}
    return  render(request, template_name = template, context=context)

def search_sentiment(request):
    template = "main/search_sentiment.html"
    # connect to elasticsearch
    es = Elasticsearch(['localhost'],port=9200)
    if 'q' in request.GET:
        query = request.GET['q']
        # search for query in elasticsearch index
        res = es.search(index="tweet-index", q = query, size=100)
        negative = []
        neutral = []
        positive = []
        for hit in res['hits']['hits']:
            dic = hit["_source"]  # get tweet as dictionary
            # Remove square brakets from hash_tag
            dic['hash_tags'] = ''.join(dic['hash_tags'])
            # parse tweet_text to extract urls
            dic['tweet_text'] = re.sub(r'http[s]?://(?:[a-zA-Z]|0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                lambda x: r'<a href="'+ re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                x.group())[0] + '"> ' + re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                x.group())[0] + '</a> ', dic['tweet_text'])
            # get sentiment of tweet text
            sentiment = TextBlob(hit['_source']['tweet_text']).polarity
            # Record sentiment score
            dic['sentiment_score'] = sentiment
            # Assign tweet to appropriate list
            if sentiment < -0.2:
                dic['sentiment'] = 'Negative'
                negative.append(hit['_source'])
            elif (sentiment > -0.21) & (sentiment < 0.2):
                dic['sentiment'] = 'Neutral'
                neutral.append(hit['_source'])
            else:
                dic['sentiment'] = 'Positive'
                positive.append(hit["_source"])
        # Sort lists
        negative = sorted(negative, key=lambda k: k['sentiment_score'])[0:10]
        neutral = sorted(neutral, key=lambda k: k['sentiment_score'])[0:10]
        positive = sorted(positive, key=lambda k: k['sentiment_score'], reverse=True)[0:10]
        # Get top 10 of each list
        context = {'negative': negative, 'neutral': neutral, 'positive': positive}

        return render(request=request, template_name = template, context=context)
    else:
        return render(request=request, template_name=template)
