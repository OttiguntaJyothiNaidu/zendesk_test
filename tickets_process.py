import json
import xlrd
import requests
import ast
import csv
import os



session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'jyothi.python@yahoo.com', 'Hetv@2010'
url = 'https://z3nplatformdevojn.zendesk.com/api/v2/tickets/create_many.json'
get_tickets_url = 'https://z3nplatformdevojn.zendesk.com/api/v2/tickets.json'
update_many_tickets_url = 'https://z3nplatformdevojn.zendesk.com/api/v2/tickets/update_many.json'
membership_default = 'https://z3nplatformdevojn.zendesk.com/api/v2/users/{user_id}/group_memberships/{membership_id}/make_default.json'
membership_default_list = 'https://z3nplatformdevojn.zendesk.com/api/v2/group_memberships.json'

fix_type = {'id': str, 'assignee_id': str, 'created_at': str, 'submitter_id': str, 'requester_id': str, \
            'subject': str, 'description': str, 'status': str, 'updated_at': str, 'due_at': str, \
            'about': str, 'business name': str, 'dept': str, 'emp id': str, 'product information': str, \
            'start date': str, 'subscription': str, 'tags': ast.literal_eval}

payloads = []
tickets_dict = {'tickets': []}
mapping_data = {"new": "New",
                "open": "Open",
                "assigned": "Open",
                "waiting": "Pending",
                "external": "On Hold",
                "engineering": "On Hold",
                "resolved": "Solved",
                "done": "Closed",
                "retracted": "Closed"}
files = [file for file in os.listdir('.') if os.path.isfile(file)]
for file in files:
    if file == "tickets.csv":
        csv_file = file
        with open(csv_file, 'r', encoding="utf-8") as file:
            for i, row in enumerate(csv.DictReader(file)):
                item = {k: fix_type[k](v) for k, v in row.items()}
                status_map_val = item["status"]
                item["status"] = mapping_data[status_map_val]
                item["assigne_id"] = 392971878711
                tickets_dict['tickets'].append(dict(item))
                if len(tickets_dict['tickets']) == 100:
                    payloads.append(json.dumps(tickets_dict))
                    tickets_dict = {'tickets': []}
            if tickets_dict['tickets']:
                payloads.append(json.dumps(tickets_dict))
for payload in payloads:
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.text))
        exit()
    print('Successfully imported multiple Tickets Records', response.text)
