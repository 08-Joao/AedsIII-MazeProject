# Código criado por Joao Victor Vieira Amora de Figueiredo[23.1.8019] e Henrique Angelo Duarte Alves[23.1.80]


# Trabalho da disciplina AEDS III Ministrada pelo professor Theo Silva Lins
#
# Obejetivos:
# Desenvolver a habilidade de programação de algoritmos em grafos.
# Reforçar o aprendizado sobre os algoritmos de busca em grafos.
# Aplicar os conhecimentos em algoritmos para resolver problemas reais.



# FYI: Na pasta Mazes, junto ao projeto, tem 7 labirintos de tamanhos variados caso não deseje criar um você mesmo. Eles vão de 13x13 até 27x27. Caso deseje adicionar mais algum labirinto, sinta-se livre para criar um e seleciona-lo na seleção de arquivos.


# Referências:
# Seleção de arquivo com GUI pelo Tkinter: https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
# Foram utilizadas as bibliotecas Tkinter para o GUI para a seleção de arquivo e Collections para deque e time para calcular o tempo de execução.
# Foi utilizado para obter o tempo de execução: https://www.programiz.com/python-programming/examples/elapsed-time
# Também foi utilizado inteligência artificial para o desenvolvimento do código, como ChatGPT
# Além dos labirintos disponibilizados pelo professor, a pasta GenericMazes contem alguns labirintos diferentes.
# DCODE para gerar labirintos diferentes, caso deseje:https://www.dcode.fr/maze-generator seguindo as seguintes configurações:
    #https://imgur.com/a/SqmCP5Q
    # "#" para representar Paredes
    # " " para representar caminho livre 
    # S de inicio e E de fim foram adicionados manualmente.


# LEGENDA
# '↑','↓','←','→' representa a direção que o algoritmo andou para chegar no ponto final
# '༝' representa o caminho que o algoritmo visitou mas retornou pois não liga com o ponto final

import sys
import math
import time
from tkinter import Tk, filedialog
from collections import deque

def ler_labirinto(filename):
    # Abrimos o arquivo do labirinto
    with open(filename, "r") as file:
        lab = file.read().splitlines()
        if lab:
            return lab
        else:
            return None

def imprimir_labirinto(lab):
    for linha in lab:
        print(linha)

# Utilizamos essa função para encontrar a posição inicial e final do labirinto (S e E)
def encontrar_posicao(labirinto, char):
    for i, linha in enumerate(labirinto):
        for j, coluna in enumerate(linha):
            if coluna == char:
                return i, j
    return None

def bfs(lab, inicio, fim):
    visitados = set()
    fila = deque([inicio])
    caminhos = {}  # Guarda o caminho percorrido
    direcoes = {
        (-1, 0): '↑',
        (1, 0): '↓',
        (0, -1): '←',
        (0, 1): '→'
    }
    
    while fila:
        x, y = fila.popleft()
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        
        if (x, y) == fim:
            # Marca o caminho percorrido no labirinto
            while (x, y) in caminhos:
                x_prev, y_prev, direcao = caminhos[(x, y)]
                if lab[x][y] not in {'S', 'E', '↑', '↓', '←', '→'}:  # Não substitua 'S', 'E' e setas
                    lab[x] = lab[x][:y] + direcao + lab[x][y+1:]
                x, y = x_prev, y_prev
            # Marca os caminhos visitados que não têm setas com "༝"
            for (vx, vy) in visitados:
                if lab[vx][vy] not in {'S', 'E', '↑', '↓', '←', '→', '༝'}:
                    lab[vx] = lab[vx][:vy] + '༝' + lab[vx][vy+1:]
            return visitados
        
        # Percorremos por todos os vizinhos possíveis do nosso ponto (x, y)
        for (nx, ny), direcao in [((x-1, y), '↑'), ((x+1, y), '↓'), ((x, y-1), '←'), ((x, y+1), '→')]:
            # Verificamos se esse possível ponto vizinho existe no labirinto
            if 0 <= nx < len(lab) and 0 <= ny < len(lab[nx]) and lab[nx][ny] != '#':
                # Se esse ponto vizinho ainda não tiver sido visitado
                if (nx, ny) not in visitados:
                    fila.append((nx, ny))
                    caminhos[(nx, ny)] = (x, y, direcao)  # Guarda a direção para retroceder
    
    return None  

def dfs(lab, inicio, fim):
    visitados = set()
    pilha = [(inicio, None)]  # Cada item é uma tupla (ponto, direção)
    caminhos = {}  # Guarda o caminho percorrido
    direcoes = {
        (-1, 0): '↑',
        (1, 0): '↓',
        (0, -1): '←',
        (0, 1): '→'
    }
    
    while pilha:
        (x, y), direcao_anterior = pilha.pop()
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        
        if (x, y) == fim:
            # Marca o caminho percorrido no labirinto
            while (x, y) in caminhos:
                x_prev, y_prev, direcao = caminhos[(x, y)]
                if lab[x][y] not in {'S', 'E', '↑', '↓', '←', '→'}:  # Não substitua 'S', 'E' e setas
                    lab[x] = lab[x][:y] + direcao + lab[x][y+1:]
                x, y = x_prev, y_prev
            # Marca os caminhos visitados que não têm setas com "༝"
            for (vx, vy) in visitados:
                if lab[vx][vy] not in {'S', 'E', '↑', '↓', '←', '→', '༝'}:
                    lab[vx] = lab[vx][:vy] + '༝' + lab[vx][vy+1:]
            return visitados
        
        # Percorremos por todos os vizinhos possíveis do nosso ponto (x, y)
        for (nx, ny), direcao in [((x-1, y), '↑'), ((x+1, y), '↓'), ((x, y-1), '←'), ((x, y+1), '→')]:
            # Verificamos se esse possível ponto vizinho existe no labirinto
            if 0 <= nx < len(lab) and 0 <= ny < len(lab[nx]) and lab[nx][ny] != '#':
                # Se esse ponto vizinho ainda não tiver sido visitado
                if (nx, ny) not in visitados:
                    pilha.append(((nx, ny), direcao))
                    caminhos[(nx, ny)] = (x, y, direcao)  # Guarda a direção para retroceder
    
    # Marca os caminhos visitados que não têm setas com "༝" após a busca completa
    for (vx, vy) in visitados:
        if lab[vx][vy] not in {'S', 'E', '↑', '↓', '←', '→', '༝'}:
            lab[vx] = lab[vx][:vy] + '༝' + lab[vx][vy+1:]
    
    return None

 
def main():
    while True:
        print("Informe o arquivo do labirinto (Cancel para sair): ")
        arquivoLab = filedialog.askopenfilename()
        
        if not arquivoLab:
            print("Fechando o programa...")
            break
        
        # Crie cópias do labirinto para BFS e DFS
        
       
        
        lab_bfs = ler_labirinto(arquivoLab)     
        lab_dfs = ler_labirinto(arquivoLab)
        
        inicio = encontrar_posicao(lab_bfs, 'S')
        fim = encontrar_posicao(lab_bfs, 'E')

        print("Inicio:", inicio)
        print("Fim:", fim)
        if not inicio or not fim:
            print("Labirinto inválido.")
            continue
        
        bfsStartTime = time.time()
        # Buscamos o caminho com a busca em largura
        caminho_bfs = bfs(lab_bfs, inicio, fim)
        print("Caminho Através da Busca por Largura:", caminho_bfs)
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Labirinto Através da Busca por Largura: ")
        imprimir_labirinto(lab_bfs)
        bfsEndTime = time.time()
        print("Tempo de execução em busca de Largura: ", bfsEndTime - bfsStartTime)
              
        dfsStartTime = time.time()  
        
        # Buscamos o caminho com a busca por profundidade
        caminho_dfs = dfs(lab_dfs, inicio, fim)
        print("Caminho Através da Busca por Profundidade:", caminho_dfs)
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Labirinto Através da Busca por Profundidade: ")
        imprimir_labirinto(lab_dfs)
        dfsEndTime = time.time() 
        print("Tempo de execução em busca de Profundidade: ", dfsEndTime - dfsStartTime)
              
              
if __name__ == '__main__':
    main()
