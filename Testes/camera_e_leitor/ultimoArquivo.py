import os

def ultimoArquivoModificado() :
    caminho = "./biometria"
    lista_arquivos = os.listdir(caminho)

    lista_datas = []
    for arquivo in lista_arquivos:
        # descobrir a data desse arquivo
        if ".dat" in arquivo:
            data = os.path.getmtime(f"{caminho}/{arquivo}")
            lista_datas.append((data, arquivo))
        
    lista_datas.sort(reverse=True)
    ultimo_arquivo = lista_datas[0]
    # print(ultimo_arquivo[1], lista_datas.__len__())
    return (ultimo_arquivo[1], lista_datas.__len__())

print(ultimoArquivoModificado())