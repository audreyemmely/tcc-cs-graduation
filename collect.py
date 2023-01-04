import json
import pandas as pd

# meyer-control, falta os composites

PROJECTS = ['achilles', 'activiti', 'androidasync', 'asynchttpclient', 'bytebuddy', 'checkstyle', 'geoserver', 'hikaricp', 'hystrix','javadriver', 'jitwatch', 'material-dialogs', 'materialdrawer', 'mockito', 'netty', 'quasar', 'restassured', 'retrolambda', 'xabberandroid']


def load_composites(project_name):
    with open("/Users/audreyvasconcelos/Downloads/analises_smells/complete_composites/" + "summarized-groups-" + project_name + ".json") as jsonfile:
        return json.load(jsonfile)


def load_smells(project_name):
    with open("/Users/audreyvasconcelos/Downloads/analises_smells/smells/" + "smells-" + project_name + ".json") as jsonfile:
        return json.load(jsonfile)


def is_candidate(composite):
    for codesmell in composite['codeSmells']:
        if codesmell['type'] in ['LongMethod']:
            return True
    return False

def convert_name(method_name):
    method_name = method_name.split(" : ")[0].split(" ", 1)[1]
    parameters = method_name[method_name.find("(")+1:method_name.find(")")]
    if parameters:
        parameters = parameters.split(", ")
        parameters = [x.split(" ")[1] for x in parameters]
        parameters = ", ".join(parameters)
        return method_name.split("(")[0] + "([" + parameters + "])"
    else:
        return method_name.split("(")[0]

def find_instances(composite, smells):
    instances = []
    elements = set()
    for refactoring in composite['refactoringsList']:
        for element in refactoring['elements']:
            if 'methodName' not in element:
                continue
            elementName = element['className'] + "." + convert_name(element['methodName'])
            elements.add((elementName, refactoring['currentCommit']['previousCommit'], refactoring['currentCommit']['commit']))
    for elementName, commit, commit_ref in elements:
        smells_in_commit = list(filter(lambda x: x['commit'] == commit, smells))
        smells_in_element = list(filter(lambda x: "codeElement" in x and x['codeElement'] == elementName, smells_in_commit))
        smell_types = []
        for smell in smells_in_element:
            smell_types.append(smell['name'])
        if "LongMethod" in smell_types:
            instances.append({
                "compositeID": composite['id'],
                "commit_before": commit,
                "commit_after": commit_ref,
                "element": elementName,
                "smellTypes": smell_types
            })
    return instances

def count_instances(instances):
    lm, lmfe = 0, 0

    for instance in instances:
        if "LongMethod" in instance['smellTypes']:
            lm += 1
        if "LongMethod" in instance['smellTypes'] and "FeatureEnvy" in instance['smellTypes']:
            lmfe += 1

    return (lm, lmfe)

def run_analyses(composite_data, smell_data):
    project_data = {
        "longmethod": 0,
        "longfeatureenvy": 0,
        "instances": list()
    }
    for composite_group in composite_data:
        for composite in composite_group['composites']:
            if is_candidate(composite):
                instances = find_instances(composite, smell_data)
                project_data['instances'] += instances
    project_data['longmethod'],  project_data['longfeatureenvy']= count_instances(project_data['instances'])
    return project_data

def to_dataframe(project_data, project):
    result = pd.json_normalize(project_data, 'instances')
    result['project'] = project
    return result


# def save_data(data, project):
#     with open("/Users/audreyvasconcelos/Downloads/analises_smells/output2/" + project + ".json", 'w') as jsonfile:
#         json.dump(data, jsonfile)


def main():
    appended_data = []
    for project in PROJECTS:
        print("Starting project", project + "...")
        composites = load_composites(project)
        smells = load_smells(project)
        project_data = run_analyses(composites, smells)
        # save_data(project_data, project)
        result = to_dataframe(project_data, project)
        appended_data.append(result)
    
    appended_data = pd.concat(appended_data,ignore_index=True)
    appended_data.to_csv('/Users/audreyvasconcelos/Downloads/analises_smells/all_smells.csv', ignore_index=True)
    print(appended_data)

if __name__ == "__main__":
    main()