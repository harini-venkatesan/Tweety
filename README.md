# Tweety - Twitter streamer and geo-located query search

Tweety is our CS172 final project that runs on a web browser that takes query terms from the user and returns the top tweets with the query. We stream tweets using [Tweepy](http://www.tweepy.org/) and perform indexing using [ElasticSearch](https://www.elastic.co/). We have also implemented sentiment analysis using [TextBlob](https://textblob.readthedocs.io/en/dev/). We then display the tweets on a world map using folium.

## Installation

To run Tweepy streamer: 

1. Create a twitter account and apply for [twitter developer account](https://developer.twitter.com/en/apply/user)
2. After creating an account, find your api key, secret key, access token, and secret token under Keys and Access Tokens and add to [stream.py](https://github.com/CS172-UCR/finalproject-tweety/blob/master/stream.py)
3. `sudo pip install tweepy` to install tweepy 
4. Run `python stream.py`
5. Collected tweets will be stored in a file named `CS_data.json'

To run the web interface files, use python 3.7.1, Django 2.1.7, Elasticsearch-dsl 6.3.1, textblob 0.15.3, and folium 0.8.2.

To install the libraries

```bash
pip3 install Django 
pip3 install elasticsearch-dsl
pip3 install folium
pip3 install -U textblob
pip3 install xlrd
python3 -m textblob.download_corpora
```
Note: Depending on the system you are using, you may need a different variation of pip3 and python3 or simply pip and python to run the installs. Make sure the versions you download are the same as the ones listed above. To view the list run ```pip list```

To run the sever: 

1. Move to [CS172_Project](https://github.com/CS172-UCR/finalproject-tweety/tree/master/CS172_Project) directory by

```bash
cd CS172_Project
```

Note: Django creates two directories with the same name by default, one
	      	is a subdirectory. You must be in the first CS172_Project
	      	directory such that you can see the following files:
	      	manage.py, db.sqlite3, main/, _pycache_/,CS172_Project

2. Run the server: 

```python
python3 manage.py runserver
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

4. At command line, navigate to the [main directory](https://github.com/CS172-UCR/finalproject-tweety) and run

```
curl -X POST "localhost:9200/_bulk" -H "Content-Type: application/json" --data-binary @tweet_index.json
```
The file name will be the file output by json_to_es.py

5. Open browser at [Localhost](http://localhost:9200/_cat/indices)

6. It should display status of ElasticSearch


To run the web browser, make sure both the server and ElasticSearch are running in the backgroud, open web browser and type: 

```
http://127.0.0.1:8000/
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
