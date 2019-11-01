import os
import sys
from datetime import datetime
import hashlib
import pymongo

mongo_uri = os.environ.get('mongo_uri', 'mongodb://localhost')

mongo_client = pymongo.MongoClient(mongo_uri)

mongo_db = mongo_client.Contest

mongo_collection = mongo_db.Contest


def update_hash(source, item):
    hash_str = source + item['name'] + item['link'] + \
        item['start_time'] + item['end_time']
    s = hashlib.sha1()
    s.update(hash_str.encode())
    item['hash'] = s.hexdigest()


def update_to_db(source, data):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for i in data:
        update_hash(source, i)
    item = {
        'source': source,
        'updated_at': time,
        'data': data
    }
    mongo_collection.update_one(
        {'source': source}, {'$set': item}, upsert=True)
    print('{file} updated at {time}'.format(
        file=os.path.basename(sys.argv[0]), time=time))
