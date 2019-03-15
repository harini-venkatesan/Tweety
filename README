# Tweety - Twitter streamer and geo-located query search

Tweety is our CS172 final project that runs on a web browser that takes query terms from the user and the location of the user and returns the top tweets with the query. We stream tweets using [Tweepy](http://www.tweepy.org/) and perform indexing using [ElasticSearch](https://www.elastic.co/). We have also implemented sentiment analysis using [TextBlob](https://textblob.readthedocs.io/en/dev/). We then display the tweets on a world map using folium.

## Installation

To run the web interface files, use python 3.7.1, Django 2.1.7 and Elasticsearch-dsl 6.3.1. 

To install Django and ElasticSearch

```bash
pip3 install Django 
pip3 install elasticsearch-dsl
```

To run the sever: 

1. Move to [CS172_Project](https://github.com/CS172-UCR/finalproject-tweety/tree/master/CS172_Project) directory by

```bash
cd CS172_Project
```

Note: there are 2 directories with the same name, one
	      	is a subdirectory. You must be in the first CS172_Project
	      	directory such that you can see the following files:
	      	manage.py, db.sqlite3, main/, _pycache_/,CS172_Project

2. Run the server: 

```python
python3 manage,py runserver
```

3. To stop the server: 
```bash
CTRL+C
```

There are multiple ways to run ElasticSeach, however it must always remain running in the background of this program. To download the package 

1. Go to [Elastic Search](https://www.elastic.co/downloads/elasticsearch). 
2. Download and unzip the file. 
3. Run 

```bash
bin/elasticsearch
``` 

4. Run 
```
curl -X POST "localhost:9200/_bulk" -H "Content-Type: application/json" --data-binary @tweets.json
```

5. Open browser at [Localhost](http://localhost:9200/_cat/indices)

6. It should display status of ElasticSearch


To run the web browser, make sure both the server and ElasticSearch are running in the backgroud, open web browser and type: 

```
http://127.0.0.1:8000/
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

