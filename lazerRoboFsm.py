try:
    import sim
except:
    print("Erro o imortar biblioteca")

import time
import numpy as np
from enum import Enum

class Estado(Enum):
    ANDAR = 1
    DESVIAR_ESQUERDA = 2
    DESVIAR_DIREITA = 3

sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000,5)

if clientID != -1:
    print("conectado ao servidor")

    #buscar os motores
    _, left_motor = sim.simxGetObjectHandle(clientID, 
                                            'Pioneer_p3dx_leftMotor',
                                            sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(clientID, 
                                            'Pioneer_p3dx_rightMotor',
                                            sim.simx_opmode_blocking)
    
    _, _ = sim.simxGetStringSignal(clientID, 
                                'Hokuyo',
                                    sim.simx_opmode_streaming)
    time.sleep(0.1)

    estado = Estado.ANDAR
    DURATION = 60 #60 segundos
    DESVIO_DURACAO = 1
    desvio_inicio = None

    start_time = time.time()

    while time.time() - start_time < DURATION:
        err, data = sim.simxGetStringSignal(clientID, 
                                'Hokuyo',
                                sim.simx_opmode_buffer)
        
        if err == sim.simx_return_ok and data:
            laser_data = sim.simxUnpackFloats(data)
            num_readings = len(laser_data)

            if num_readings == 0:
                continue

            start_angle = -120
            angle_step = 240 / num_readings

            front_dist = []
            left_dist = []
            right_dist = []

            for i, dist in enumerate(laser_data):
                angle = start_angle + i * angle_step
                if -20 <= angle <= 20:
                    front_dist.append(dist)
                elif 45 <= angle <= 90:
                    left_dist.append(dist)
                elif -90 <= angle <= -45:
                    right_dist.append(dist)

            MIN_DISTANCE = 0.5

            obstacle_ahead = any(d < MIN_DISTANCE for d in front_dist)
            
            if estado == Estado.ANDAR:
                if obstacle_ahead:
                    avg_left = np.mean(left_dist) if left_dist else 0
                    avg_right = np.mean(right_dist) if right_dist else 0

                    if avg_left > avg_right:
                        estado = Estado.DESVIAR_ESQUERDA
                        print("Mudando estado para desviar esquerda")
                    else:
                        estado = Estado.DESVIAR_DIREITA
                        print("Mudando estado para desviar direita")

                    desvio_inicio = time.time()
                else:
                    sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    2.0,
                                                    sim.simx_opmode_streaming)
                    sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    2.0,
                                                    sim.simx_opmode_streaming)
            elif estado == Estado.DESVIAR_ESQUERDA:
                sim.simxSetJointTargetVelocity(clientID, 
                                                left_motor, 
                                                -1.5,
                                                sim.simx_opmode_streaming)
                sim.simxSetJointTargetVelocity(clientID, 
                                                right_motor, 
                                                1.5,
                                                sim.simx_opmode_streaming)
                if time.time() - desvio_inicio >= DESVIO_DURACAO:
                    estado = Estado.ANDAR
                    print("Voltando a andar")
            elif estado == Estado.DESVIAR_DIREITA:
                sim.simxSetJointTargetVelocity(clientID, 
                                                left_motor, 
                                                1.5,
                                                sim.simx_opmode_streaming)
                sim.simxSetJointTargetVelocity(clientID, 
                                                right_motor, 
                                                -1.5,
                                                sim.simx_opmode_streaming)
                if time.time() - desvio_inicio >= DESVIO_DURACAO:
                    estado = Estado.ANDAR
                    print("Voltando a andar")

        time.sleep(0.1)

    sim.simxSetJointTargetVelocity(clientID, 
                                    left_motor, 
                                    0,
                                    sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, 
                                    right_motor, 
                                    0,
                                    sim.simx_opmode_blocking)
    
    sim.simxFinish(clientID)
else:
    print("falha ao conectar no servidor")

print("Programa finalizado")