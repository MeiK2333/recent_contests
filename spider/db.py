import os
from datetime import datetime

import pymongo

mongo_uri = os.environ.get('mongo_uri', 'mongodb://localhost')

mongo_client = pymongo.MongoClient()

mongo_db = mongo_client.Contest

mongo_collection = mongo_db.Contest


def update_to_db(source, data):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item = {
        'source': source,
        'updated_at': time,
        'data': data
    }
    mongo_collection.update_one(
        {'source': source}, {'$set': item}, upsert=True)
