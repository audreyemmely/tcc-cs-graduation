from pymongo import MongoClient

uri = 'mongodb://localhost:27017'

client = MongoClient(uri)

db = client.get_database('refactoringsdb')
collection = db.get_collection('smells')

element = 'integration.tests.JoinCollectionAndMapIT.should_persist_join_collection_and_map'
commit_before = '429c142097888b459a68d55836506d79609c1aa1'

filter = {'codeElement':element, 'commit':commit_before}

cursor = collection.find(filter)

for each_doc in cursor:
    print(each_doc['metrics'])