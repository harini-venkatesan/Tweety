# Input: json file with tweets from stream.py
# Ouput: json file to perform bulk load to elasticsearch

import json

outfile = open('/path/to/output/file.json', 'w')

with open('/path/to/input/file.json') as f:
  for line in f:
    # change "_index":"tweets"
    meta =  { "index" : { "_index" : "tweets", "_type" : "tweet", "_id" : json.loads(line)['tweet_id'] } } 
    outfile.write(json.dumps(meta))
    outfile.write('\n')
    outfile.write(json.dumps(json.loads(line)))
    outfile.write('\n')

outfile.close()
