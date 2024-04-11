# Instalem as bibliotecas
# pip install Pillow
# pip install numpy
import os
import numpy as np
from PIL import Image #Obs: Dizer no relatorio que esta utilizando a biblioteca PIL

def corrigir_orientacao(imagem):
    # Verifica se a orientação da imagem está correta
    if imagem.width > imagem.height:
        # Rotaciona a imagem se estiver na orientação errada
        imagem = imagem.transpose(Image.ROTATE_90)
    return imagem

def Numero_Mais_Repetido(lista):
    numero_255 = 0
    numero_0 = 0
    for i in range(len(lista)):
        if lista[i] == 255:
            numero_255 = numero_255 + 1
        else:
            numero_0 = numero_0 + 1
    
    if numero_0 >= numero_255:
        return 0
    else:
        return 255

def ajustar_IMG(matriz, nome_arquivo):
    altura = len(matriz)
    largura = len(matriz[0])
    print(altura,largura)
    
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever cabeçalho PBM
        arquivo.write("P1\n")
        arquivo.write(f"{largura} {altura}\n")
        
        # Escrever valores dos pixels
        for linha in range(altura):
            for coluna in range(largura):
                if str(matriz[linha][coluna]) == "True":
                    arquivo.write(str(0) + "")
                else:
                    arquivo.write(str(1) + "")
            arquivo.write("\n")

def matriz_para_pbm(matriz, nome_arquivo):
    altura = len(matriz)
    largura = len(matriz[0])
    
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever cabeçalho PBM
        arquivo.write("P1\n")
        arquivo.write(f"{largura} {altura}\n")
        
        # Escrever valores dos pixels
        for linha in matriz:
            for pixel in linha:
                arquivo.write(str(pixel) + "")
            arquivo.write("\n")


def filtro_mediana(matriz, tamanhoDoFiltro):
    altura = len(matriz)
    largura = len(matriz[0])
    nova_matriz = []
    
    for y in range(altura):
        nova_linha = []
        for x in range(largura):
            vizinhos = []
            for j in range(-tamanhoDoFiltro // 2, tamanhoDoFiltro // 2 + 1):
                for i in range(-tamanhoDoFiltro // 2, tamanhoDoFiltro // 2 + 1):
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        vizinhos.append(matriz[y + j][x + i])
            nova_linha.append(sorted(vizinhos)[len(vizinhos) // 2])
        nova_matriz.append(nova_linha)
    
    return nova_matriz

def dilatar(matriz, matrizTransformacao, tamanhoTransformador):
    altura = len(matriz)
    largura = len(matriz[0])
    nova_matriz = []
    ajuste = tamanhoTransformador // 2
    cont = 0
    
    for y in range(altura):
        nova_linha = []
        for x in range(largura):
            cont = 0
            for j in range(-(tamanhoTransformador // 2), tamanhoTransformador // 2 + 1):
                if cont == 1:
                    break
                for i in range(-(tamanhoTransformador // 2), tamanhoTransformador // 2 + 1):
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        if matriz[y+j][x+i] == str(matrizTransformacao[j+ajuste][i+ajuste]):
                            cont = 1
                            break
            if cont == 1:
                nova_linha.append(1)
            else:
                nova_linha.append(0)
        nova_matriz.append(nova_linha)
    
    return nova_matriz
                    

def ler_imagem_pbm(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        # Remover comentários (linhas começando com #)
        linhas = [linha.strip() for linha in linhas if not linha.startswith('#')]
        
        # Ignorar cabeçalho (primeira linha contém o formato e possíveis comentários)
        largura, altura = map(int, linhas[1].split())
        
        # Os pixels começam a partir da terceira linha
        for linha in linhas[2:]:
            matriz.append(linha)
        
    
    return matriz


# Exemplo de uso
#nome_arquivo = 'imagemComSalEPimenta.pbm'
nome_arquivo_corrigido = 'imagemComSalEPimentaCorrigido.pbm'
nome_arquivo_filtrado = 'imagemSemSalEPimenta.pbm'
#caminho_completo = os.path.join(os.getcwd(), nome_arquivo)

### Ler a imagem corrigida
#img = Image.open(nome_arquivo)
### transformar em um array
#matriz = np.array(img)
# Trocar os True e False por 0 e 1
#ajustar_IMG(matriz,nome_arquivo_corrigido)

matrizTrans =  [[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1]]
# Colocar em uma nova matriz a nova imagem corrigida
matriz_corrigida = ler_imagem_pbm(nome_arquivo_corrigido)
# Usar o filtro da mediana
matriz_filtrada = filtro_mediana(matriz_corrigida,3)
# Transforma numa imagem
matriz_dilatada = dilatar(matriz_filtrada, matrizTrans, 9)
matriz_para_pbm(matriz_dilatada,"imagemDilatada.pbm")