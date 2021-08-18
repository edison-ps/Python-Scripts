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
            
            body = { 
                'object': row['AAVSO'].upper(),
                'ra': row['RA'],
                'dec': row['DEC'],
                'maxMag': float(row['Maximo (V)']),
                'minMag': float(row['Minimo (V)']),
                'period': row['Periodo (dias)'],
                'type': row['Tipo']
                
            }

            req = requests.post(api + '/objects', data = json.dumps(body), headers = headers)

            if (req.status_code == 201):
                print(req.status_code, ' ', req.json())
            else:
                print(req.status_code, '  ERRO -> ', body)
