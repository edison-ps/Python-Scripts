import requests
import csv
import json
import os

api = 'http://192.168.54.51:3000'
csvFile = "./Observations/full-Observations.csv"

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
            
            airMass = row['AMASS']

            if (airMass != ''):
                airMass = float(row['AMASS'])
            
            body = { 
                'object': row['NAME'].upper(),
                'filter': row['FILT'],
                'comparation': row['CNAME'],
                'jd': float(row['DATE']),
                'mag': float(row['MAG']),
                'mErr': float(row['MERR']),
                'airMass': airMass
            }

            if (body['object'][0] == 'V' and body['object'][-4] != ' '):
                body['object'] = body['object'][:-3] + ' ' + body['object'][-3:]

            if (airMass == ''):
                body.pop('airMass')

            req = requests.post(api + '/observations', data = json.dumps(body), headers = headers)

            if (req.status_code == 201):
                print(req.status_code, ' ', req.json())
            else:
                print(req.status_code, '  ERRO -> ', body)
                print(req.json())
else:
    print(req.status_code, ' ', req.json())