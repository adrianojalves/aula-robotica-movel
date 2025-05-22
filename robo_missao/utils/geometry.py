import numpy as np
import math

def distancia(p1, p2):
    return np.linalg.norm(p1 - p2)

def angulo_para_alvo(pos_robo, ang_robo, alvo):
    delta = alvo - pos_robo
    ang_desejado = math.atan2(delta[1], delta[0])
    erro = ang_desejado - ang_robo
    return math.atan2(math.sin(erro), math.cos(erro))  # normaliza