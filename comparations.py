import requests
import csv
import json
import os

api = 'http://192.168.54.51:3000'
csvFile = "./Objects/Objects.txt"

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

    with open(csvFile, 'r') as obs:

        reader = csv.DictReader(obs, delimiter = ';')
        
        for row in reader:
            
            if (row['Comp'] != ''):
                body = { 
                    'comparation': row['Comp'].upper(),
                    'ra': row['RAComp'],
                    'dec': row['DECComp'],
                    'mag': float(row['MagComp']),
                    'chart': row['Carta']
                }

                if (body['chart'] == ''):
                    body.pop('chart')

                req = requests.post(api + '/comparations', data = json.dumps(body), headers = headers)

                if (req.status_code == 201):
                    print(req.status_code, ' ', req.json())
                else:
                    print(req.status_code, '  ERRO -> ', body)
                    print(req.json())
