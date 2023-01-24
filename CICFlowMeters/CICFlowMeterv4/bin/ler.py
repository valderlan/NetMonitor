import os

root, dirs, arquivos = next(os.walk("./csv/"))#'.'
# root : Imprime diretórios apenas do que você especificou.
# dirs : Imprime subdiretórios da raiz.
# arquivos : Imprime todos os arquivos da raiz e diretórios.
extensoes = ['csv']
#arquivos = os.listdir(pasta)
print(root)
'''for i in arquivos:
    print(type(i))
    if extensoes == []:
        print(i)
    else:
        extensao = i.split('.')[-1]
        if extensao in extensoes:
            print(i)'''