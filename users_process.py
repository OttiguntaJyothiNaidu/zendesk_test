import json
import xlrd
import requests
import ast
import csv
import os
session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'jyothi.python@yahoo.com', 'Hetv@2010'
url = 'https://z3nplatformdevojn.zendesk.com/api/v2/users/create_many.json'


fix_type = {'id': int, 'name': str, 'email': str, 'notes':str,'group':str,'api_subscription':str,\
            'role': str,'employee_id':int,'promotion_code':str,'active':bool,'tags':ast.literal_eval,\
            'organization_id':ast.literal_eval}


payloads = []
users_dict = {'users': []}
files = [file for file in os.listdir('.') if os.path.isfile(file)]
for file in files:
    if file == "users.csv":
        csv_file = file
        with open ('users.csv','r',encoding="utf-8") as csvFile:
            csvReader = csv.DictReader(csvFile)
            for csvRow in csvReader:
                org_id = ast.literal_eval(csvRow['organization_id'])
                if type(csvRow['organization_id']) == type(0):
                    pass
                if type(org_id) == type([]):
                    for individual_org_item in org_id:
                        individual_org_item = int(individual_org_item)
                        print (individual_org_item)
                        users_dict['users'].append({
                            'name':csvRow["name"],
                            'email':csvRow["email"],
                            'notes':csvRow['notes'],
                            'group':csvRow['group'],
                            'api_subscription':csvRow['api_subscription'],
                            'role':csvRow['role'],
                            'employee_id':csvRow['employee_id'],
                            'promotion_code':csvRow['promotion_code'],
                            'active':csvRow['active'],
                            # 'organization_id':int(individual_org_item),
                            'tags':ast.literal_eval(csvRow['tags'])})
                else:
                    users_dict['users'].append({
                        'name': csvRow["name"],
                        'email': csvRow["email"],
                        'notes': csvRow['notes'],
                        'group': csvRow['group'],
                        'api_subscription': csvRow['api_subscription'],
                        'role': csvRow['role'],
                        'employee_id': csvRow['employee_id'],
                        'promotion_code': csvRow['promotion_code'],
                        'active': csvRow['active'],
                        # 'organization_id': org_id,
                        'tags': ast.literal_eval(csvRow['tags'])})

                if len(users_dict['users']) == 100:
                    payloads.append(json.dumps(users_dict))
                    users_dict = {'users': []}

            if users_dict['users']:
                payloads.append(json.dumps(users_dict))

for payload in payloads:
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.text))
        exit()
    print('Successfully imported a batch of users',response.text)