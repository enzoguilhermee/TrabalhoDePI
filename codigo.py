import os
from PIL import Image #Obs: Dizer no relatorio que esta utilizando a biblioteca PIL

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
                arquivo.write(str(pixel) + " ")
            arquivo.write("\n")


def filtro_mediana(matriz, tamanhoDoFiltro, altura, largura):
    print(altura, largura)
    nova_matriz = []
    
    for y in range(altura):
        nova_linha = []
        for x in range(largura):
            vizinhos = []
            for j in range(-tamanhoDoFiltro // 2, tamanhoDoFiltro // 2 + 1):
                for i in range(-tamanhoDoFiltro // 2, tamanhoDoFiltro // 2 + 1):
                    print(y+j, x+i)
                    if 0 <= y + j < altura and 0 <= x + i < largura:
                        vizinhos.append(matriz[y + j][x + i])
            nova_linha.append(sorted(vizinhos)[len(vizinhos) // 2])
        nova_matriz.append(nova_linha)
    
    return nova_matriz

def ler_imagem_pbm(caminho):
    matriz = []
    with open(caminho, 'r') as arquivo:
        linhas = arquivo.readlines()
        
        # Remover comentários do arquivo
        linhas = [linha.strip() for linha in linhas if not linha.startswith('#')]
        
        # Extrair largura e altura da imagem
        largura, altura = map(int, linhas[1].split())
        
        linha_certa = []
        cont = 0
        # Ler os pixels da imagem
        for linha in linhas[3:]:
            if (largura-1 >= cont):
                cont = cont + len(linha)
                linha_certa.append(linha)
            else:
                linha_junta = ''.join(linha_certa)
                matriz.append(linha_junta)
                linha_certa.clear
                linha_junta.clear
                cont = 0
        
    
    return matriz, largura, altura


# Exemplo de uso
nome_arquivo = 'imagemComSalEPimenta.pbm'
caminho_completo = os.path.join(os.getcwd(), nome_arquivo)
matriz, largura, altura = ler_imagem_pbm(caminho_completo)

nome_nova_imagem = "imagemSemSalEPimenta.pbm"


print("Dimensões da imagem:", largura, "x", altura)
print("Matriz da imagem:")