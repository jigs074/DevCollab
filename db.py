import pymongo

from pymongo import MongoClient

client = "mongodb+srv://ericwengew:<password>@cluster0.f7b0fmd.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
db = MongoClient(client, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    db.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)