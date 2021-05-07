from typing import List, Tuple

def lefetivo_tubo(l: float, r: float, m: int) -> float:
    """

    :param l: comprimento do tubo
    :param r: raio do tubo
    :param m: numero de aberturas no tubo

    :return: comprimento efetivo do tubo

    """
    return l + 0.6*r*m

def lefetivo_ressoador(l: float, r: float) -> float:
    """

    :param l: comprimento do gargalo do ressoador
    :param r: raio do gargalo do ressoador

    :return: comprimento efetivo do gargalo do ressoador

    """
    return l + 1.45*r

def incerteza_triangular(v: float) -> float:
    """

    :param v: variacao com relacao a melhor estimativa, por exemplo
        'esse objeto tem 20cm mais ou menos 1cm de altura' onde u=1cm

    :return: incerteza padrao associada a variacao dada para uma funcao de
        distribuicao de probabilidade triangular

    """
    return v/(6**0.5)

def incerteza_quadrada(v: float) -> float:
    """

    :param v: variacao com relacao a melhor estimativa, por exemplo
        'esse objeto tem 20cm mais ou menos 1cm de altura' onde u=1cm

    :return: incerteza padrao associada a variacao dada para uma funcao de
        distribuicao de probabilidade quadrada

    """
    return v/(3**0.5)

def incerteza_padrao(l: List[Tuple[float, float]]) -> float:
    """

    :param l: lista de tuplas que descrevem a incerteza de um parametro
        o primeiro elemento da tupla deve ser o coeficiente de sensibilidade
        e o segundo elemento da tupla deve ser a incerteza padrao

    :return: incerteza padrao combinada para uma grandeza

    """
    result_squared = 0
    for i in l:
        result_squared += i[0]**2 * i[1]**2
    result = result_squared ** (1/2)
    return result
