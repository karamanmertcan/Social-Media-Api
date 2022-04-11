from pymongo import MongoClient
import certifi


uri = "mongodb+srv://mertcankaraman:mertcan123@cluster0.33wcq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(
    uri, tlsCAFile=certifi.where())
