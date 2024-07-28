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

def marcar_caminho(lab, caminho, direcoes, caminho_explorado):
    for (x, y), direcao in direcoes.items():
        if lab[x][y] not in ('S', 'E'):
            lab[x][y] = direcao
    for (x, y) in caminho_explorado:
        if lab[x][y] not in ('S', 'E', '↑', '↓', '←', '→'):
            lab[x][y] = '༝'

def bfs(lab, inicio, fim):
    fila = deque([(inicio, [], {})])  # Inclui o caminho e as direções percorridas
    visitados = set([inicio])
    explorados = []  # Lista para armazenar todos os nós visitados

    while fila:
        no, caminho, direcoes = fila.popleft()
        i, j = no
        explorados.append(no)  # Adiciona o nó atual à lista de nós visitados
        if no == fim:
            return caminho + [fim], explorados, direcoes
        vizinhos = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        direcoes_vizinhos = {
            (i+1, j): '↓',
            (i-1, j): '↑',
            (i, j+1): '→',
            (i, j-1): '←'
        }
        for vizinho in vizinhos:
            x, y = vizinho
            if 0 <= x < len(lab) and 0 <= y < len(lab[0]) and lab[x][y] not in ('#', '█') and vizinho not in visitados:
                fila.append((vizinho, caminho + [no], {**direcoes, **{vizinho: direcoes_vizinhos[(x, y)]}}))
                visitados.add(vizinho)
    return None, explorados, direcoes

def dfs(lab, inicio, fim):
    pilha = [(inicio, [], {})]  # Inclui o caminho e as direções percorridas
    visitados = set([inicio])
    explorados = []  # Lista para armazenar todos os nós visitados

    while pilha:
        no, caminho, direcoes = pilha.pop()
        i, j = no
        explorados.append(no)  # Adiciona o nó atual à lista de nós visitados
        if no == fim:
            return caminho + [fim], explorados, direcoes
        vizinhos = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        direcoes_vizinhos = {
            (i+1, j): '↓',
            (i-1, j): '↑',
            (i, j+1): '→',
            (i, j-1): '←'
        }
        for vizinho in vizinhos:
            x, y = vizinho
            if 0 <= x < len(lab) and 0 <= y < len(lab[0]) and lab[x][y] not in ('#', '█') and vizinho not in visitados:
                pilha.append((vizinho, caminho + [no], {**direcoes, **{vizinho: direcoes_vizinhos[(x, y)]}}))
                visitados.add(vizinho)
    return None, explorados, direcoes

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

        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        bfsStartTime = time.time()
        # Buscamos o caminho com a busca em largura
        caminho_bfs, explorados_bfs, direcoes_bfs = bfs(lab_bfs, inicio, fim)
        marcar_caminho(lab_bfs, caminho_bfs, direcoes_bfs, explorados_bfs)
        print("Labirinto após Busca por Largura:")
        imprimir_labirinto(lab_bfs)
        print("Nós Visitados na Busca por Largura:", explorados_bfs)
        bfsEndTime = time.time()
        print("Tempo de execução em busca de Largura: ", bfsEndTime - bfsStartTime)

        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        dfsStartTime = time.time()
        # Buscamos o caminho com a busca por profundidade
        caminho_dfs, explorados_dfs, direcoes_dfs = dfs(lab_dfs, inicio, fim)
        marcar_caminho(lab_dfs, caminho_dfs, direcoes_dfs, explorados_dfs)
        print("Labirinto após Busca por Profundidade:")
        imprimir_labirinto(lab_dfs)
        print("Nós Visitados na Busca por Profundidade:", explorados_dfs)
        dfsEndTime = time.time()
        print("Tempo de execução em busca de Profundidade: ", dfsEndTime - dfsStartTime)

if __name__ == '__main__':
    main()
