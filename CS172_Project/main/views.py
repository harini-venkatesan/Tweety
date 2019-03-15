from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
import json, re, string, xlrd
from textblob import TextBlob
import folium # for map
import pandas as pd


connections.create_connection()
# Create your views here.
def homepage(request):
    return render(request = request, template_name = "main/home.html")

def search_tweet(request):
    template = 'main/search.html'
    es = Elasticsearch(['localhost'],port=9200)
    if 'q' in request.GET:
        query = request.GET['q']
        res = es.search(index="tweets", q = query, size=100)
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
            # get sentiment of tweet text
            sentiment = TextBlob(hit['_source']['tweet_text']).polarity
            if sentiment < -0.5:
                dic['sentiment'] = 'Negative'
            elif (sentiment > -0.5) & (sentiment < 0.5):
                dic['sentiment'] = 'Neutral'
            else:
                dic['sentiment'] = 'Positive'
            
            results.append(hit["_source"])

        context = {'results': results, 'query': query}
        return render(request=request, template_name=template, context=context)
    else:
        return render(request=request, template_name=template)

def world_wide(request):
    template = "main/worldwide.html"

    # Open xlsx file
    loc = ("worldcities.xlsx") 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 

    Location = []
    for line in open('CS_data.json', 'r'):
        Location.append(json.loads(line))

    clear_location = []
    m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=3)

    for i in range (0, len(Location)):
        if Location[i]['Location'] != None:
            location = Location[i]['Location']
            clear_location = location.split()
            for row_num in range(sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    if row_value[1] == clear_location[0]:
                            lat = row_value[2]
                            lon = row_value[3]
                            tweet_text = Location[i]['tweet_text']
                            username = Location[i]['user_name']
                            folium.Marker([lat, lon], "%s: %s "%(tweet_text,username)).add_to(m)
    context = {'m': m._repr_html_()}
    return  render(request, template_name = template, context=context)

def search_sentiment(request):
    template = "main/search_sentiment.html"
    es = Elasticsearch(['localhost'],port=9200)
    res = es.search(index="tweets", size=110) #change to index size
    negative = []
    neutral = []
    positive = []
    url = ''
    for hit in res['hits']['hits']:
        # get json object - tweet
        dic = hit["_source"] 
        # Remove square brakets from hash_tag
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
        # get sentiment of tweet text
        sentiment = TextBlob(hit['_source']['tweet_text']).polarity
        dic['sentiment_score'] = sentiment
        if sentiment < -0.5:
            dic['sentiment'] = 'Negative'
            negative.append(hit['_source'])
        elif (sentiment > -0.5) & (sentiment < 0.5):
            dic['sentiment'] = 'Neutral'
            neutral.append(hit['_source'])
        else:
            dic['sentiment'] = 'Positive'
            positive.append(hit["_source"])
    negative = sorted(negative, key=lambda k: k['sentiment_score'], reverse=True)[0:10]
    neutral = sorted(neutral, key=lambda k: k['sentiment_score'], reverse=True)[0:10]
    positive = sorted(positive, key=lambda k: k['sentiment_score'], reverse=True)[0:10]
    # Get top 10 of each list
    context = {'negative': negative, 'neutral': neutral, 'positive': positive}

    return render(request=request, template_name = template, context=context)
