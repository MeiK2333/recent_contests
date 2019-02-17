import os
from datetime import datetime

import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)

mongo_uri = os.environ.get('mongo_uri', 'mongodb://localhost')

mongo_client = pymongo.MongoClient()

mongo_db = mongo_client.Contest

mongo_collection = mongo_db.Contest


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/contests.json')
def contests():
    include = request.args.getlist('include')
    exclude = request.args.getlist('exclude')

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    data = []
    for oj in mongo_collection.find():
        oj.pop('_id')
        # 排除项
        if oj['source'] in exclude:
            continue
        if include == [] or oj['source'] in include:
            for item in oj['data']:
                item['source'] = oj['source']
                # 只返回未结束的比赛
                if item['end_time'] >= now:
                    data.append(item)

    data = sorted(data, key=lambda item: item['start_time'])
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
