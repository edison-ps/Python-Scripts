import requests
import os
import mysql.connector
import time

import random

from mysql.connector import Error

database = 'Test_Adhara'
url = os.getenv('SENSORS_API')

def writeDataBase(data):
    
    try:

        connection = mysql.connector.connect (host = os.getenv('ADHARA_SERVER'),
                                                user = os.getenv('ADHARA_USER'),
                                                password = os.getenv('ADHARA_PASSWORD'),
                                                port = os.getenv('ADHARA_PORT'),
                                                database = database)

        commandInsert = """INSERT INTO Sensores
                    (altitude, chuva, chuvaNivel, co2, luminosidade, pressao, temperaturaExterna, temperaturaInterna, umidade, uv)
                VALUES
                    ("""
        commandData = str(data['altitude'])  + ',' + str(data['chuva'])  + ',' +  str(data['chuvaNivel'])  + ','  + str(data['co2'])  + ',' + str(data['luminosidade'])  + ','  + str(data['pressao'])  + ',' + str(data['temperaturaExterna'])  + ',' + str(data['temperaturaInterna'])  + ',' + str(data['umidade'])  + ',' + str(data['uv']) + ')'
        sql = commandInsert + commandData
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

        # print(cursor.rowcount, ' Registros inseridos')

        cursor.close()

    except Error as erro:

        print ('Falha ao inserir dados na tabela {}: {}'.format(database, erro))

    finally:

        if (connection.is_connected()):

            cursor.close()
            connection.close()
            # print ('Conexão com o MariaDB encerrada')
            # print()

while True:

    req = requests.get(url)
    
    if (req.status_code == 200):

        writeDataBase(req.json())
        # values = {
        #     'altitude': random.randint(0, 600),
        #     'chuva': random.randint(0, 1),
        #     'chuvaNivel': random.randint(0, 1023),
        #     'co2': random.randint(0, 60),
        #     'luminosidade': random.randint(0, 1023),
        #     'pressao': random.random() * 1000,
        #     'temperaturaExterna': random.random() * 40,
        #     'temperaturaInterna': random.random() * 40,
        #     'umidade': random.randint(0, 99),
        #     'uv': random.randint(0, 9)
        # }
        # writeDataBase(values)
    
    time.sleep(600)