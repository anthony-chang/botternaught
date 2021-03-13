from pymongo import MongoClient
from data_aggregator import DATABASE_NAME, COLLECTION_NAME

client = MongoClient('localhost', 27017)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
collection.drop()
print('{} dropped'.format(collection.name))