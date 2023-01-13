from pymongo import MongoClient
import pandas as pd
from codeElement import CodeElement

uri = 'mongodb://localhost:27017'

client = MongoClient(uri)
names = ['activiti', 'jacksondatabind', 'bytebuddy']

db = client.get_database('refactoringsdb')
collection = db.get_collection('smells')
for name in names:
    filter = {'projectName': name}

    results = collection.find(filter)

    methods = set()

    for smell in results:
        if 'codeElement' in smell and smell['codeElement'].find("("):
            methods.add(smell['codeElement'])

    # print('Methods: {}'.format(len(methods)))

    smelly_methods = []
    for method in methods:
        print('Method for: {}'.format(method))
        for smell in results:
            print(smell['codeElement'])
            if smell['codeElement'] == method:
                print('tem longmethod')
                codeElement = CodeElement()
                codeElement.method = method
                codeElement.projectName = name
                codeElement.metrics.append(smell['metrics'])
                codeElement.smells.append(smell['name'])
                codeElement.commit = smell['commit']
                smelly_methods.append(codeElement)

    # print(len(smelly_methods))

    for index, method in smelly_methods:
        for smell in results:
            if smell['codeElement'] == method and smell['name'] != 'LongMethod' and smell['commit'] == method.commit:
                smelly_methods[index].smells.append(smell['name'])
                smelly_methods[index].metrics.append(smell['metrics'])

# print('save csv')
# smelly_methods.to_csv('/Users/audreyvasconcelos/Desktop/tcc/{}_smells.csv'.format(name), index=False)
