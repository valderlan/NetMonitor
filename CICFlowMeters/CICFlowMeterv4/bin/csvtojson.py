import csv
import json
import os

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # ler arquivos csv
    with open(csvFilePath, encoding = 'utf-8') as csvf:
        # carregar dados do arquivo csv usando o leitor de dicionário da biblioteca csv
        csvReader = csv.DictReader(csvf)
        # converter cada linha csv em dict python
        for row in csvReader:
            # adicione este dict python ao array json
            jsonArray.append(row)
    # converter python jsonArray para JSON String e gravar no arquivo
    with open(jsonFilePath, 'w',encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray,indent=4)
        jsonf.write(jsonString)



csvFilePath = r'data.csv'
jsonFilePath = r'.data1.json'



csv_to_json(csvFilePath, jsonFilePath)

