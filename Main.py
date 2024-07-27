# Código criado por Joao Victor Vieira Amora de Figueiredo[23.1.8019] e Henrique Angelo Duarte Alves[23.1.8028]


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

def imprimir_labirinto(lab):
    for linha in lab:
        print(''.join(linha))  # Juntando os caracteres para imprimir como uma linha

def ler_labirinto(filename):
    with open(filename, "r") as file:
        lab = file.read().splitlines()
        if lab:
            return [list(linha) for linha in lab]  # Convertendo cada linha em uma lista de caracteres
        else:
            return None

def encontrar_posicao(lab, char):
    for i, linha in enumerate(lab):
        for j, c in enumerate(linha):
            if c == char:
                return (i, j)
    return None

def bfs(lab, start, end):
    rows, cols = len(lab), len(lab[0])
    queue = deque([(start, [start])])  # Fila com a posição inicial e o caminho percorrido
    visited = set([start])  # Conjunto de posições visitadas
    
    # Movimentos possíveis: direita, esquerda, para cima, para baixo
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        (current, path) = queue.popleft()
        
        if current == end:
            return path  # Retorna o caminho se a posição final for alcançada
        
        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_position = (next_row, next_col)
            
            if 0 <= next_row < rows and 0 <= next_col < cols and lab[next_row][next_col] != '#' and next_position not in visited:
                queue.append((next_position, path + [next_position]))
                visited.add(next_position)
    
    return None  # Retorna None se não houver caminho

def dfs(lab, start, end):
    rows, cols = len(lab), len(lab[0])
    stack = [(start, [start])]  # Pilha com a posição inicial e o caminho percorrido
    visited = set([start])  # Conjunto de posições visitadas
    
    # Movimentos possíveis: direita, esquerda, para cima, para baixo
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        (current, path) = stack.pop()
        
        if current == end:
            return path  # Retorna o caminho se a posição final for alcançada
        
        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_position = (next_row, next_col)
            
            if 0 <= next_row < rows and 0 <= next_col < cols and lab[next_row][next_col] != '#' and next_position not in visited:
                stack.append((next_position, path + [next_position]))
                visited.add(next_position)
    
    return None  # Retorna None se não houver caminho

def marcar_caminho(lab, caminho):
    if caminho:
        for row, col in caminho:
            if lab[row][col] not in ('S', 'E'):
                lab[row][col] = '•'
                
def main():
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    
    while True:
        print("Informe o arquivo do labirinto (Cancel para sair): ")
        arquivoLab = filedialog.askopenfilename()
        
        if not arquivoLab:
            print("Fechando o programa...")
            break
        
        # Crie cópias do labirinto para BFS e DFS
        lab_bfs = ler_labirinto(arquivoLab)     
        lab_dfs = ler_labirinto(arquivoLab)
        
        if not lab_bfs or not lab_dfs:
            print("Falha ao ler o labirinto.")
            continue
        
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
        marcar_caminho(lab_bfs, caminho_bfs)
        imprimir_labirinto(lab_bfs)
        bfsEndTime = time.time()
        print("Tempo de execução em busca de Largura: ", bfsEndTime - bfsStartTime)
              
        dfsStartTime = time.time()  
        
        # Buscamos o caminho com a busca por profundidade
        caminho_dfs = dfs(lab_dfs, inicio, fim)
        print("Caminho Através da Busca por Profundidade:", caminho_dfs)
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Labirinto Através da Busca por Profundidade: ")
        marcar_caminho(lab_dfs, caminho_dfs)
        imprimir_labirinto(lab_dfs)
        dfsEndTime = time.time() 
        print("Tempo de execução em busca de Profundidade: ", dfsEndTime - dfsStartTime)
              
if __name__ == '__main__':
    main()
