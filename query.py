from pymongo import MongoClient
import pandas as pd

smells = pd.read_csv('/Users/audreyvasconcelos/Desktop/tcc/all_smells.csv')

uri = 'mongodb://localhost:27017'

client = MongoClient(uri)

db = client.get_database('refactoringsdb')
collection = db.get_collection('smells')

print('Mongo Query...')
appended_data = []
i = 0
while i < len(smells):
    element = smells['element'][i]
    commit_before = smells['commit_before'][i]
    filter = {'codeElement':element, 'commit':commit_before}
    cursor = collection.find(filter)
    metrics = cursor[0]['metrics']
    df_metric = pd.json_normalize(metrics) 
    appended_data.append(df_metric)
    i+=1

appended_data = pd.concat(appended_data,ignore_index=True)

print('Saving csv...')
appended_data = appended_data.rename_axis('index1').reset_index()
smells = smells.rename_axis('index1').reset_index()

smells_metrics = pd.merge(smells, appended_data, how = 'outer')
smells_metrics.drop(['index1'],axis=1, inplace=True)
smells_metrics.to_csv('/Users/audreyvasconcelos/Downloads/analises_smells/smells_metrics.csv', index=False)