import os
from datetime import datetime

import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app, supports_credentials=True)

mongo_uri = os.environ.get("mongo_uri", "mongodb://localhost")

mongo_client = pymongo.MongoClient(mongo_uri)

mongo_db = mongo_client.Contest

mongo_collection = mongo_db.Contest


@app.route("/")
def index():
    data = {
        "GitHub": "https://github.com/MeiK2333/recent_contests",
        "message": "The web api allows cross-domain access, you can reference this data directly, but please indicate the data source",
        "contests_link": f"https://contests.sdutacm.cn/contests.json",
        "updated_at": [
            {"source": oj["source"], "updated_at": oj["updated_at"]}
            for oj in mongo_collection.find()
        ],
    }
    return jsonify(data)


@app.route("/contests.json")
def contests():
    include = request.args.getlist("include") + request.args.getlist("include[]")
    exclude = request.args.getlist("exclude") + request.args.getlist("exclude[]")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    data = []
    for oj in mongo_collection.find():
        oj.pop("_id")
        # 排除项
        if oj["source"] in exclude:
            continue
        if include == [] or oj["source"] in include:
            for item in oj["data"]:
                item["source"] = oj["source"]
                # 只返回未结束的比赛
                if item["end_time"] >= now:
                    # 解析成 ISO 8801 标准的格式，以便 JS 等其他语言处理
                    item["start_time"] = datetime.strptime(
                        item["start_time"], "%Y-%m-%d %H:%M:%S"
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                    item["end_time"] = datetime.strptime(
                        item["end_time"], "%Y-%m-%d %H:%M:%S"
                    ).strftime("%Y-%m-%dT%H:%M:%SZ")
                    data.append(item)

    data = sorted(data, key=lambda item: item["start_time"])
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
