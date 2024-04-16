# Instalem as bibliotecas
# pip install Pillow
# pip install numpy
import os
import numpy as np
from PIL import Image #Obs: Dizer no relatorio que esta utilizando a biblioteca PIL

def InicializarMatriz(altura,largura):
    matriz = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            linha.append(str(0))
        matriz.append(linha)

    return matriz

# Necessario para encontrar a mediana em uma lista
# Pegando o numero mais repetido, é possivel encontrar a mediana
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

# A biblioteca "PIL", tem a função "open" que ler a imagem como True e False
# Mas para consertar e virar uma matriz binaria, usa-se essa função
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

# Função necessaria para criar uma nova imagem a partir de uma matriz.
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

# Função necessaria para remover os ruidos
# OBS: Demora uns 30 segundos...
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
                        vizinhos.append(matriz[y + j][x + i])
            nova_linha.append(Numero_Mais_Repetido(vizinhos))
        nova_matriz.append(nova_linha)
    
    return nova_matriz

# Função para dilatar as letras, a partir de uma mascara
# Obs: A mascara deve ser quadrada e com numeros primos, ou seja, 3x3, 5x5, 7x7
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
                        if (matriz[y+j][x+i] == str(matrizTransformacao[j+ajuste][i+ajuste])) and (str(matrizTransformacao[j+ajuste][i+ajuste]) == str(1)):
                            cont = 1
                            break
            if cont == 1:
                nova_linha.append(str(1))
            else:
                nova_linha.append(str(0))
        nova_matriz.append(nova_linha)
    
    return nova_matriz

# Função para erodir as letras, a partir de uma mascara
# Obs: A mascara deve ser quadrada e com numeros primos, ou seja, 3x3, 5x5, 7x7
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

                    
# Ler uma imagem pre-processada e coloca numa matriz
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

# Função para contar as palavras

def contar_palavras(matriz, matrizContador):
    altura = len(matriz)
    largura = len(matriz[0])
    #Todas as imagens começam na altura = 179
    y = 179
    linha = 0
    palavras = 0

    dentro_dePalavra = 0
    mesmaLinha = 0

    paragrafo = 1

    # Enquanto a altura atual não for superior a altura maxima, continue
    while (y < altura):
        dentro_dePalavra = 0
        paragrafo = paragrafo + 1
        for x in range(largura):
            cont = 0
            # Cada iteração é passada uma mascara de 17x1
            for j in range(-9,9):
                if 0 <= y+j < altura:
                    # Se encontrar alguma parte preta, pare, pois encontrou alguma palavra, ou ta dentro de uma
                    if matriz[y+j][x] == str(matrizContador[j+9][0]):
                        break
                    else:
                        cont = cont + 1
            # Se pelomenos encontrar uma bit preto, ainda estará dentro de uma palavra
            if cont != 18 and dentro_dePalavra != 1 and y != altura-3 :
                if (mesmaLinha == 0):
                    mesmaLinha = 1
                    linha = linha + 1
                palavras = palavras + 1
                dentro_dePalavra = 1
            # Se todas os bit forem branco, nao esta dentro da palavra
            if cont >= 18:
                dentro_dePalavra = 0
        # Cada linha tem uma altura alternada
        if paragrafo >= 2:
            mesmaLinha = 0
            y = y + 39
            paragrafo = 0
        else:
            mesmaLinha = 0
            paragrafo = paragrafo + 1
            y = y + 38
    
    return palavras



def contar_coluna(matriz, matrizContador):
    altura = len(matriz)
    largura = len(matriz[0])
    coluna = 0
    mesmaColuna = 1
    espaco = 0
    y = 179
    for x in range(largura):
        cont = 0
        for j in range(-9,9):
            if matriz[y+j][x] == str(matrizContador[j+9][0]):
                break
            else:
                cont = cont + 1
        if cont != 18:
            mesmaColuna = 0
            espaco = 0
        else:
            if cont >= 18:
                espaco = espaco + 1
                if (espaco >= 34 and espaco <= 36) and mesmaColuna == 0:
                    print("Matriz: ", y+3, x)
                    coluna = coluna + 1
                    mesmaColuna = 1
    
    return coluna



# Mascara 17x1 para passar em cada palavra
contador = [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]

# Mascara 13x13, usada para dilatar e erodir
matrizB =  [    [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1],
                [1,1,1,1,1,1,1,1,1,1,0,1,1]
                ]


# Exemplo de uso
i = 3
nome_arquivo = (f'Imagem{i}.pbm')
nome_arquivo_corrigido = (f'Imagem{i}Corrigido.pbm')
#

### Ler a imagem com "open"
img = Image.open(nome_arquivo)
### transformar em um array de True e False
matriz = np.array(img)
### Trocar os True e False por 0 e 1
#matriz_ajustada = ajustar_IMG(matriz, nome_arquivo_corrigido)

# Aplica o filtro da mediana
### Tempo de 30 segundos ou menos
#matrizA = filtro_mediana(matriz_ajustada,3)

### Aplica a dilatação com mascara da MatrizB, 11x11
#matrizC = dilatar(matrizA, matrizB, 11)
#matriz_para_pbm(matrizC, "Imagem1Dilatada11x11.pbm")
#matriz_para_pbm(matrizC, f"Imagem{i}Dilatada11x11.pbm")
matrizC = ler_imagem_pbm(f'Imagem{i}Dilatada11x11.pbm')
print(contar_palavras(matrizC, contador))
print(contar_coluna(matrizC, contador))

# Para que cada palavra vire um quadrado, utilize essa função contar_palavras:
# É demorada, mas espere kkk