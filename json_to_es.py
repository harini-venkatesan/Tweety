# Input: json file with tweets from stream.py
# Ouput: json file to perform bulk load to elasticsearch

import json

outfile = open('tweet_index.json', 'w')

with open('tweet_data.json', 'r') as f:
  for line in f:
    # change "_index":"tweets"
    meta =  { "index" : { "_index" : "tweet-index", "_type" : "tweet", "_id" : json.loads(line)['tweet_id'] } } 
    outfile.write(json.dumps(meta))
    outfile.write('\n')
    outfile.write(json.dumps(json.loads(line)))
    outfile.write('\n')

outfile.close()
