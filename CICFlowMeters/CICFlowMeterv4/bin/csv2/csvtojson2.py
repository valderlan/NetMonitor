import csv
import json
import os
#import shutil
#from tkinter.filedialog import askdirectory

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
    #my_dir ='../valderlan/NetMonitor/CICFlowMeters/CICFlowMeterv4/bin/json/'
    #fname=os.path.join(my_dir,jsonFilePath)
    with open("../json/"+jsonFilePath, 'w',encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray,indent=4)
        jsonf.write(jsonString)
        #print(jsonFilePath)
        #save_file = str(askdirectory(initialdir="~/valderlan/NetMonitor/CICFlowMeters/CICFlowMeterv4/bin/json/"))
        #shutil.move(jsonFilePath,save_file)

root, dirs, arquivos = next(os.walk("."))#'.'
# root : Imprime diretórios apenas do que você especificou.
# dirs : Imprime subdiretórios da raiz.
# arquivos : Imprime todos os arquivos da raiz e diretórios.
extensoes = ['csv']
#arquivos = os.listdir(pasta)
#print(root)
for i in arquivos:
    
    if extensoes == []:
        print(i)
    else:
        extensao = i.split('.')[-1]
        if extensao in extensoes:
            nome, meio, fim=str(i).split(".")
            csvFilePath = i
            jsonFilePath = nome + '.json'
            csv_to_json(csvFilePath, jsonFilePath)
            