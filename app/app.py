from bson import json_util
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

MONGO_HOST = 'nosqldb'
MONGO_PORT = 27017
MONGO_DB = 'admin'
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'example'

client: MongoClient = MongoClient(
    MONGO_HOST,
    MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    authSource=MONGO_DB
)
db = client[MONGO_DB]

collection = db.mycollection


@app.route('/<key>', methods=['GET', 'PUT'])
def manage_data_update_get(key):
    if request.method == 'PUT':
        new_value = request.get_json()
        new_value = new_value.get(key)
        if not new_value:
            return jsonify(
                {'message': f'Такого ключа {key} не существует'}
            ), 400
        collection.update_one(
            {key: {"$exists": True}}, {"$set": {key: new_value}}
        )
        return jsonify({key: new_value}), 200
    else:
        data = collection.find_one({key: {"$exists": True}})
        if data:
            return json_util.dumps({key: data[key]})
        else:
            return jsonify({"message": "Data not found"}), 404


@app.route('/', methods=['POST'])
def manage_date_create():
    if request.method == 'POST':
        data = request.get_json()
        key = list(data.keys())[0]
        check_key = collection.find_one({key: {"$exists": True}})
        if check_key:
            return jsonify({"message": "Такой ключ уже создан"}), 400
        collection.insert_one(data)
        return jsonify({"message": "Data created"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
