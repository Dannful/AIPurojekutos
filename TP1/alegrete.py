import numpy as np


def compute_mse(b: float, w: float, data: np.array):
    """
    Calcula o erro quadratico medio
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    def predicted_function(x: float):
        return b + w * x

    error = 0
    for x in data:
        error += (predicted_function(x[0]) - x[1])**2
    error /= len(data)
    return error


def step_gradient(b: float, w: float, data: np.array, alpha: float):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de b e w.
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de b e w, respectivamente
    """

    def current_function(x: float):
        return b + w * x

    bias_derivative = 0
    weight_derivative = 0
    for x in data:
        bias_derivative += 2 * (current_function(x[0]) - x[1])
        weight_derivative += 2 * x[0] * (current_function(x[0]) - x[1])

    new_bias = b - alpha * bias_derivative / len(data)
    new_weight = w - alpha * weight_derivative / len(data)

    return new_bias, new_weight


def fit(data: np.array, b: float, w: float, alpha: float, num_iterations: int):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de b e w.
    Ao final, retorna duas listas, uma com os b e outra com os w
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os b e outra com os w obtidos ao longo da execução
    """

    biases = [b]
    weights = [w]

    for _ in range(num_iterations):
        b, w = step_gradient(b, w, data, alpha)
        biases.append(b)
        weights.append(w)

    return biases, weights
