import json

with open("/Users/audreyvasconcelos/Desktop/tcc/smells-checkstyle.json") as jsonfile:
    checkstyle = json.load(jsonfile)

methods = set()

for smell in checkstyle:
    codeelement = smell['codeElement']
    if codeelement != None and codeelement.find("("):
        methods.add(codeelement)

    new_methods = list(methods)
    smelly_methods = []
    # for method in methods:        
    for smell in checkstyle:
        if smell['codeElement'] == new_methods[0] and smell['name'] == 'LongMethod':
            print('tem longmethod')
                # codeElement = CodeElement()
                # codeElement.method = method
                # codeElement.projectName = 'checkstyle'
                # codeElement.metrics.append(smell['metrics'])
                # codeElement.smells.append(smell['name'])
                # codeElement.commit = smell['commit']
                # smelly_methods.append(codeElement)

    # print(len(smelly_methods))

    # for index, method in smelly_methods:
    #     for smell in checkstyle:
    #         if smell['codeElement'] == method and smell['name'] != 'LongMethod' and smell['commit'] == method.commit:
    #             smelly_methods[index].smells.append(smell['name'])
    #             smelly_methods[index].metrics.append(smell['metrics'])

# print('save csv')
# smelly_methods.to_csv('/Users/audreyvasconcelos/Desktop/tcc/{}_smells.csv'.format(name), index=False)

