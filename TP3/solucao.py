from __future__ import annotations

import heapq
from typing import Callable, Optional, Set, Tuple


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """

    def __init__(
        self, estado: str, pai: Optional[Nodo], acao: Optional[str], custo: int
    ):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Nodo):
            return False
        if value.estado == self.estado and value.acao == self.acao:
            return True
        return False

    def __hash__(self) -> int:
        if self.acao is not None:
            return hash(self.estado + self.acao + str(self.custo))
        return hash(self.estado + str(self.custo))

    def __lt__(self, other: Nodo) -> bool:
        return other.custo > self.custo


class State:
    def __init__(self, stringState):
        self.state = []
        self.state.append(list(stringState[0:3]))
        self.state.append(list(stringState[3:6]))
        self.state.append(list(stringState[6:9]))

    def to_string(self):
        out = ""
        for i in self.state:
            for j in i:
                out += j
        return out

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, State):
            return False
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] != value.state[i][j]:
                    return False
        return True

    def get_blank(self) -> Tuple[int, int]:
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] == "_":
                    return i, j
        return -1, -1

    def clone(self) -> State:
        return State(self.to_string())


estado_objetivo = "12345678_"


def is_objetivo(nodo: Nodo) -> bool:
    return nodo.estado == estado_objetivo


def sucessor(estado: str) -> Set[Tuple[str, str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    state = State(estado)
    line, column = state.get_blank()

    result = set[Tuple[str, str]]()
    if column != 0:
        copy = state.clone()
        copy.state[line][column], copy.state[line][column - 1] = (
            copy.state[line][column - 1],
            copy.state[line][column],
        )
        result.add(("esquerda", copy.to_string()))

    if column != 2:
        copy = state.clone()
        copy.state[line][column], copy.state[line][column + 1] = (
            copy.state[line][column + 1],
            copy.state[line][column],
        )
        result.add(("direita", copy.to_string()))

    if line != 0:
        copy = state.clone()
        copy.state[line][column], copy.state[line - 1][column] = (
            copy.state[line - 1][column],
            copy.state[line][column],
        )
        result.add(("acima", copy.to_string()))

    if line != 2:
        copy = state.clone()
        copy.state[line][column], copy.state[line + 1][column] = (
            copy.state[line + 1][column],
            copy.state[line][column],
        )
        result.add(("abaixo", copy.to_string()))

    return result


def expande(nodo: Nodo) -> Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    sucessores = sucessor(nodo.estado)
    result = set()
    for acao, estado in sucessores:
        result.add(Nodo(estado, nodo, acao, nodo.custo + 1))
    return result


def reconstroi_movimentos(nodo: Nodo) -> list[str]:
    movimentos = []
    while nodo is not None and nodo.pai is not None:
        movimentos.insert(0, nodo.acao)
        nodo = nodo.pai
    return movimentos


def is_solvable(estado: str) -> bool:
    inversions = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if (
                estado[i] != "_"
                and estado[j] != "_"
                and int(estado[i]) > int(estado[j])
            ):
                inversions += 1
    return inversions % 2 == 0


def astar(estado: str, heurisica: Callable[[str], int]) -> list[str]:
    # Como o 8-puzzle e bipartido, podemos testar para ver se o estado
    # possui solucao preliminarmente, salvando de termos de expandir 10!/2
    # nodos para exaurir a fronteira.
    if not is_solvable(estado):
        return None # type: ignore
    explorado = set[Nodo]()
    fronteira = list[Tuple[int, Nodo]]()
    fronteira.append((0, Nodo(estado, None, None, 0)))
    while fronteira:
        # escolhe o melhor da fronteira
        _, v = fronteira.pop(0)
        
        # se chegou no estado objetivo
        if is_objetivo(v):
            # caminha na arvore reconstruindo os movimentos
            return reconstroi_movimentos(v)
        # senao, explora o estado do nodo v
        if v not in explorado: # nodos sao considerados iguais se seus estado sao iguais (ver __eq__ em Nodo)
            # adiciona v aos explorados
            explorado.add(v)
            # expande v
            novos_nodos = expande(v)
            for nodo in novos_nodos:
                # insere na priority queue, usando custo (g) + heurisica (h) para ordenamento (f)
                heapq.heappush(fronteira, (nodo.custo + heurisica(nodo.estado), nodo))
    # desnecessario, a validacao de is_solvable garante que nunca sera expandido todos os 
    # estados alcancaveis sem encontrar uma solucao
    return None # type: ignore

# Retorna a quantidade de pecas em posicoes erradas
def distancia_hamming(estado: str) -> int:
    dist = 0
    for i,v in enumerate(estado):
        if estado_objetivo[i] != v:
            dist += 1
    return dist

def astar_hamming(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    return astar(estado, distancia_hamming)

# Representacao bizarra da array contendo a posicao "desejada" de cada peca
posicoes_objetivo = {
    '1': (0,0), '2': (0,1), '3': (0,2), #123
    '4': (1,0), '5': (1,1), '6': (1,2), #456
    '7': (2,0), '8': (2,1), '_': (2,2)  #78_
}

# Retorna a distancia euclidiana entre cada peca e sua posicao desejada
def distancia_manhattan(estado: str) -> int:
    dist = 0
    for i,v in enumerate(estado):
        # Converte o valor de uma posicao na array [0,8] para a posicao
        # em uma matriz 3x3 [(0,0), (2,2)]
        p_i = i // 3 # linha
        p_j = i  % 3 # coluna
        o_i , o_j = posicoes_objetivo[v] # valores "desejados" de p_i, p_j
        dist += abs(o_i - p_i) + abs(o_j - p_j)
    return dist

def astar_manhattan(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    return astar(estado, distancia_manhattan)


# opcional,extra
def bfs(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# opcional,extra
def dfs(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# opcional,extra
def astar_new_heuristic(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
