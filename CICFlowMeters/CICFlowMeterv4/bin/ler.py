import os

path, pasta, arquivos = next(os.walk("./csv/"))#'.'
extensoes = ['csv']
#arquivos = os.listdir(pasta)

for i in arquivos:
    print(i)
    if extensoes == []:
        print(i)
    '''else:
        extensao = i.split('.')[-1]
        if extensao in extensoes:
            print(i)'''