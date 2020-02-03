import json
import xlrd
import requests
import ast
import csv
import csv
session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'jyothi.python@yahoo.com', 'Hetv@2010'
post_single_org_url = 'https://z3nplatformdevojn.zendesk.com/api/v2/organizations.json'
post_many_org_url = 'https://z3nplatformdevojn.zendesk.com/api/v2/organizations/create_many.json'


payloads = []
orgs_dict = {'organizations': []}
fix_type = {'id': bool, 'name': str, 'details': str, \
            'notes': str,'merchant_id':str,'tags':ast.literal_eval,'domain_names':ast.literal_eval}
with open("organizations.csv","r",encoding="utf-8", newline='') as file:
    for i, row in enumerate(csv.DictReader(file)):
        item = {k: fix_type[k](v) for k, v in row.items()}
        for tuple_value in item["domain_names"]:
            if tuple_value.startswith("("):
                item["domain_names"] = tuple_value.replace("(", "").replace(")", "")
        orgs_dict['organizations'].append(dict(item))

        if len(orgs_dict['organizations']) == 100:
            payloads.append(json.dumps(orgs_dict))
            orgs_dict = {'organizations': []}

    if orgs_dict['organizations']:
        payloads.append(json.dumps(orgs_dict))

for payload in payloads:
    response = session.post(post_many_org_url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.text))
        print('Import failed with status {}'.format(response.status_code))
        exit()
    print('Successfully imported a batch of Orgnizations',response.text)
    print ("Successfully imported a batch of Orgnizations",response.status_code)