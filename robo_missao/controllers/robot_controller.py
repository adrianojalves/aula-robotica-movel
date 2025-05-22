import sim
import time
import numpy as np

class RobotController:
    def __init__(self, client_id):
        self.client_id = client_id
        _, self.robo = sim.simxGetObjectHandle(client_id, 'Pioneer_p3dx', sim.simx_opmode_blocking)
        _, self.motorE = sim.simxGetObjectHandle(client_id, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)
        _, self.motorD = sim.simxGetObjectHandle(client_id, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)
        self.laser = 'Hokuyo'

        sim.simxGetObjectPosition(client_id, self.robo, -1, sim.simx_opmode_streaming)
        sim.simxGetObjectOrientation(client_id, self.robo, -1, sim.simx_opmode_streaming)
        sim.simxGetStringSignal(client_id, self.laser, sim.simx_opmode_streaming)
        time.sleep(1)

    def get_posicao_e_orientacao(self):
        _, pos = sim.simxGetObjectPosition(self.client_id, self.robo, -1, sim.simx_opmode_buffer)
        _, ang = sim.simxGetObjectOrientation(self.client_id, self.robo, -1, sim.simx_opmode_buffer)
        return np.array([pos[0], pos[1]]), ang[2]

    def ler_laser_frontal(self):
        _, dados_str = sim.simxGetStringSignal(self.client_id, self.laser, sim.simx_opmode_buffer)
        if dados_str:
            dados = sim.simxUnpackFloats(dados_str)
            return dados[len(dados)//2]
        return None

    def definir_velocidades(self, vE, vD):
        sim.simxSetJointTargetVelocity(self.client_id, self.motorE, vE, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.client_id, self.motorD, vD, sim.simx_opmode_oneshot)

    def parar(self):
        self.definir_velocidades(0, 0)
