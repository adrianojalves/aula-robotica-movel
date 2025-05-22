from configs.config import VEL_LIN, VEL_ANG, DIST_PARADA
from utils.geometry import distancia, angulo_para_alvo

def ir_para(robot_ctrl, destino, posicoes):
    pos, ang = robot_ctrl.get_posicao_e_orientacao()
    posicoes.append(tuple(pos))

    erro_ang = angulo_para_alvo(pos, ang, destino)

    if abs(erro_ang) > 0.2:
        vE = -VEL_ANG if erro_ang > 0 else VEL_ANG
        vD = VEL_ANG if erro_ang > 0 else -VEL_ANG
    else:
        dist_laser = robot_ctrl.ler_laser_frontal()
        if dist_laser and dist_laser < 0.5:
            vE = VEL_LIN * 0.2
            vD = VEL_LIN * -0.5
        else:
            vE = VEL_LIN
            vD = VEL_LIN

    robot_ctrl.definir_velocidades(vE, vD)

    return distancia(pos, destino) < DIST_PARADA