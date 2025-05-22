from controllers.navigation import ir_para
from configs.config import POS_BASE, POS_VITIMA
from utils.plot import plotar_trajeto
from services.mission_state import MissionState
import time

class MissionManager:
    def __init__(self, robot_ctrl):
        self.robot_ctrl = robot_ctrl
        self.estado = MissionState.IR_PARA_VITIMA
        self.posicoes = []

    def executar(self):
        while True:
            if self.estado == MissionState.IR_PARA_VITIMA:
                chegou = ir_para(self.robot_ctrl, POS_VITIMA, self.posicoes)
                if chegou:
                    print("Chegou à vítima.")
                    self.estado = MissionState.RETORNAR_BASE
                    time.sleep(1)

            elif self.estado == MissionState.RETORNAR_BASE:
                chegou = ir_para(self.robot_ctrl, POS_BASE, self.posicoes)
                if chegou:
                    print("Retornou à base.")
                    self.estado = MissionState.FIM
                    time.sleep(1)

            elif self.estado == MissionState.FIM:
                self.robot_ctrl.parar()
                plotar_trajeto(self.posicoes, POS_BASE, POS_VITIMA)
                break

            time.sleep(0.05)