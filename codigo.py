# Instalem as bibliotecas
# pip install Pillow
# pip install numpy
import os
import numpy as np
from PIL import Image #Obs: Dizer no relatorio que esta utilizando a biblioteca PIL



def Numero_Mais_Repetido(lista):
    numero_1 = 0
    numero_0 = 0
    for i in range(len(lista)):
        if lista[i] == str(1):
            numero_1 = numero_1 + 1
        else:
            numero_0 = numero_0 + 1
    
    if numero_0 >= numero_1:
        return str(0)
    else:
        return str(1)

def ajustar_IMG(matriz, nome_arquivo):
    altura = len(matriz)
    largura = len(matriz[0])
    print(altura,largura)
    nova_matriz = []
    
    with open(nome_arquivo, 'w') as arquivo:
        # Escrever cabeçalho PBM
        arquivo.write("P1\n")
        arquivo.write(f"{largura} {altura}\n")
        
        # Escrever valores dos pixels
        for linha in range(altura):
            nova_linha = []
            for coluna in range(largura):
                if str(matriz[linha][coluna]) == "True":
                    nova_linha.append(str(0))
                    arquivo.write(str(0) + "")
                else:
                    nova_linha.append(str(1))
                    arquivo.write(str(1) + "")
            nova_matriz.append(nova_linha)
            arquivo.write("\n")
    
    return nova_matriz

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
            for j in range(-(tamanhoDoFiltro // 2), tamanhoDoFiltro // 2 + 1):
                for i in range(-(tamanhoDoFiltro // 2), tamanhoDoFiltro // 2 + 1):
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        print("Matriz y+j: ",y+j, " x+i: ", x+i, " ", matriz[y+j][x+i] )
                        vizinhos.append(matriz[y + j][x + i])
            print(Numero_Mais_Repetido(vizinhos))
            nova_linha.append(Numero_Mais_Repetido(vizinhos))
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
                nova_linha.append(str(1))
            else:
                nova_linha.append(str(0))
        nova_matriz.append(nova_linha)
    
    return nova_matriz

def erosao(matriz, matrizTransformacao, tamanhoTransformador):
    altura = len(matriz)
    largura = len(matriz[0])
    nova_matriz = []
    ajuste = tamanhoTransformador // 2
    cont = 0
    invalido = 0
    
    for y in range(altura):
        nova_linha = []
        for x in range(largura):
            cont = 0
            invalido = 0
            for j in range(-(tamanhoTransformador // 2), tamanhoTransformador // 2 + 1):
                if invalido == 1:
                    break
                for i in range(-(tamanhoTransformador // 2), tamanhoTransformador // 2 + 1):
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        if matriz[y+j][x+i] == str(matrizTransformacao[j+ajuste][i+ajuste]):
                            cont = cont + 1
                    else:
                        invalido = 1
                        break
            if cont == tamanhoTransformador*tamanhoTransformador:
                nova_linha.append(str(1))
            else:
                if invalido == 1:
                    nova_linha.append(matriz[y][x])
                else:
                    nova_linha.append(str(0))
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

matrizTrans =  [[1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1]
                ]

matrizTeste = [ ['1','1','1','0','0','0','0','0','0'],
                ['1','1','1','0','0','0','0','0','0'],
                ['1','1','1','0','0','0','0','0','0'],
                ['1','1','1','0','0','0','0','0','0'],
                ['1','1','1','0','0','0','0','0','0'],
                ['1','1','1','0','1','0','1','0','1'],
                ['1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1'],
                ['1','1','1','1','1','1','1','1','1']]

# Exemplo de uso
nome_arquivo = 'imagemComRuidos.pbm'
nome_arquivo_corrigido = 'imagemComRuidosCorrigido.pbm'
nome_arquivo_filtrado = 'imagemSemRuidos.pbm'
nome_arquivo_dilatado = 'imagemDilatado9x9.pbm'

### Ler a imagem corrigida
img = Image.open(nome_arquivo)
### transformar em um array
matriz = np.array(img)
### Trocar os True e False por 0 e 1
matriz_ajustada = ajustar_IMG(matriz, nome_arquivo_corrigido)

matrizA = dilatar(matriz_ajustada, matrizTrans, 3)
matrizB = erosao(matrizA, matrizTrans, 3)
matrizC = dilatar(matrizB, matrizTrans, 9)

matriz_para_pbm(matrizC, nome_arquivo_dilatado)

def letra_para_ponto(nome_arquivo_letra):
    # Ler a imagem com a letra
    img_letra = Image.open(nome_arquivo_letra)
    
    # Converter para tons de cinza, se necessário
    if img_letra.mode != 'L':
        img_letra = img_letra.convert('L')
    
    # Aplicar um limiar para binarizar a imagem
    limite = 128
    img_binaria = img_letra.point(lambda p: p > limite and 255)
    
    # Encontrar o centroide da região branca
    matriz_binaria = np.array(img_binaria)
    altura, largura = matriz_binaria.shape
    soma_x = 0
    soma_y = 0
    total_pixels = 0
    
    for y in range(altura):
        for x in range(largura):
            if matriz_binaria[y][x] == 255:  # Pixel branco
                soma_x += x
                soma_y += y
                total_pixels += 1
    
    # Calcular as coordenadas do centroide
    if total_pixels > 0:
        centroide_x = soma_x / total_pixels
        centroide_y = soma_y / total_pixels
        return (centroide_x, centroide_y)
    else:
        return None

#Chamamos essa função passando o nome do arquivo da imagem da letra, e ela retornará as coordenadas do ponto representativo da letra.

#EXEMPLO: 
#
'''
nome_arquivo_letra = 'letraA.png'  # Substitua pelo nome do arquivo da sua imagem com a letra
ponto_letra = letra_para_ponto(nome_arquivo_letra)
if ponto_letra is not None:
    print("Coordenadas do ponto representativo da letra:", ponto_letra)
else:
    print("Não foi possível encontrar o ponto representativo da letra.")
'''
#  Essa função assume que a letra é branca e o fundo é preto na imagem binarizada. Se a imagem estiver ao contrário, você pode ajustar o limiar ou inverter as cores antes de chamar a função.


'''
Para implementar a compressão de imagens usando a transformada de blocos e identificar linhas e palavras, você pode seguir os seguintes passos:

Dividir a imagem em pequenos blocos não sobrepostos de mesmo tamanho (por exemplo, 8 × 8).
Aplicar uma transformada 2-D a cada bloco (por exemplo, transformada discreta de Fourier ou transformada de Walsh-Hadamard).
Identificar linhas de texto analisando os coeficientes transformados para cada bloco.
Usar os espaçamentos entre dois pontos para definir a distância entre palavras.
Determinar se há uma ou duas colunas de texto com base na distribuição dos espaçamentos entre palavras.
Aqui está uma implementação básica desses passos:
'''

import math

def fft2(bloco):
    """Calcula a transformada 2D de Fourier de um bloco."""
    altura, largura = len(bloco), len(bloco[0])
    coeficientes = [[0j] * largura for _ in range(altura)]

    # Loop para cada coeficiente na transformada
    for v in range(altura):
        for u in range(largura):
            somatorio = 0
            # Loop para cada pixel no bloco
            for y in range(altura):
                for x in range(largura):
                    # Aplicação da fórmula da transformada de Fourier
                    somatorio += bloco[y][x] * complex(math.cos(-2 * math.pi * ((u * x / largura) + (v * y / altura))),
                                                        math.sin(-2 * math.pi * ((u * x / largura) + (v * y / altura))))
            coeficientes[v][u] = somatorio

    return coeficientes

def encontrar_palavras(coeficientes):
    """Identifica os espaçamentos entre palavras com base nos coeficientes."""
    # Implementação necessária com base na análise dos coeficientes
    pass

def encontrar_numero_colunas(coeficientes):
    """Determina o número de colunas com base nos coeficientes."""
    # Implementação necessária com base na análise dos coeficientes
    pass

def compressao_transformada_blocos(imagem, tamanho_bloco=8):
    """Comprime a imagem dividindo-a em blocos e aplicando a transformada 2D."""
    altura, largura = len(imagem), len(imagem[0])
    coeficientes_comprimidos = []

    # Passo 1: Dividir a imagem em blocos
    for y in range(0, altura, tamanho_bloco):
        for x in range(0, largura, tamanho_bloco):
            bloco = [linha[x:x+tamanho_bloco] for linha in imagem[y:y+tamanho_bloco]]

            # Passo 2: Aplicar a transformada 2-D
            coeficientes = fft2(bloco)

            # Passo 3: Identificar linhas de texto
            soma_coeficientes = sum(abs(coef) for linha in coeficientes for coef in linha)
            if soma_coeficientes > limiar_linha:
                linha = {'bloco': bloco, 'coeficientes': coeficientes}
                coeficientes_comprimidos.append(linha)

    # Passo 4: Identificar espaçamentos entre palavras
    for linha in coeficientes_comprimidos:
        encontrar_palavras(linha['coeficientes'])

    # Passo 5: Determinar o número de colunas
    numero_colunas = encontrar_numero_colunas(coeficientes_comprimidos[0]['coeficientes'])

    return coeficientes_comprimidos, numero_colunas

# Exemplo de uso
'''
imagem = [[0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 0, 0, 0, 0, 0],
          [0, 1, 1, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0]]
'''
limiar_linha = 10  # Ajuste o limiar conforme necessário

# Comprimir a imagem usando a transformada de blocos
coeficientes_comprimidos, numero_colunas = compressao_transformada_blocos(imagem)

# Visualizar o resultado
print("Número de colunas:", numero_colunas)

'''
Nesta implementação, a função fft2d calcula a transformada 2D de Fourier de um bloco utilizando apenas operações matemáticas básicas. Em seguida, a função compressao_transformada_blocos divide a imagem em blocos, calcula a transformada de Fourier para cada bloco e identifica linhas de texto com base na soma dos coeficientes transformados.


Neste código, adicionei duas funções novas: encontrar_palavras e encontrar_numero_colunas. Essas funções serão responsáveis por implementar os passos 4 e 5, respectivamente. No exemplo de uso, após chamar a função compressao_transformada_blocos, o número de colunas é exibido como resultado. Você precisará implementar o corpo dessas funções com base na análise dos coeficientes da transformada de blocos para identificar os espaçamentos entre palavras e determinar o número de colunas.
'''
