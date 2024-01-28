from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request, jsonify, json, Blueprint
uri = "mongodb+srv://ericwengew:RrOhGb7guZDqkmTh@cluster0.f7b0fmd.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.Blogpost_Database
def delete_field(username, post):
    collection = db[username]
    filter_query = {'_id':post['_id']}

    collection.delete_one(filter_query)
    
def edit_field(username, post):
    collection = db[username]
    filter_query = {'_id':post['_id']}
    collection.update_one(filter_query, {'$set': {'content': post['content']}})

def export_to_mongodb(username, new_post): #export one post to collection:username
    collection = db[username]
    result = collection.insert_one(new_post)

def import_from_mongodb(username): #import as json file
    collection = db[username]
    data_from_mongodb = list(collection.find())
    json_data = json.dumps(data_from_mongodb,indent=4)

    with open('data.json','w') as f:
        f.write(json_data)

