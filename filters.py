import requests
import csv
import json
import os

api = 'http://192.168.54.51:3000'
csvFile = "../../MySQL/Filters-utf8.csv"

headers = {'content-type': 'application/json'}

login = {
    'email': os.getenv('EMAIL'),
    'password': os.getenv('PASSWORD')
}

req = requests.post(api + '/login', data = json.dumps(login), headers = headers)

if (req.status_code == 200):

    headers = {
        'content-type': 'application/json',
        'Authorization': req.json()['token']
        }

    with open(csvFile, 'r') as filters:

        reader = csv.DictReader(filters, delimiter = ';')
        
        for row in reader:
            
            body = { 
                'name': row['name'],
                'description': row['description'],
                'wavelength': float(row['wavelength']),
                'unitId': int(row['unitId'])
            }
        
            req = requests.post(api + '/filters', data = json.dumps(body), headers = headers)

            print(req.status_code, ' ', req.json())
        

