try:
    import sim
except:
    print("Erro o imortar biblioteca")

import time
import numpy as np
import math

IR_PARA_DESTINO = 0
CONTORNAR_OBSTACULO = 1

ESQUERDA=0
DIREITA=1

sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000,5)

if clientID != -1:
    print("conectado ao servidor")

    _, left_motor = sim.simxGetObjectHandle(clientID, 
                                                'Pioneer_p3dx_leftMotor',
                                                sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(clientID, 
                                                'Pioneer_p3dx_rightMotor',
                                                sim.simx_opmode_blocking)
    _, robo_handle = sim.simxGetObjectHandle(clientID, 
                                                'Pioneer_p3dx',
                                                sim.simx_opmode_blocking)
    
    sim.simxGetObjectPosition(clientID,
                            robo_handle,
                            -1,
                            sim.simx_opmode_streaming)
    sim.simxGetObjectOrientation(clientID,
                            robo_handle,
                            -1,
                            sim.simx_opmode_streaming)
    sim.simxGetStringSignal(clientID, 
                                'Hokuyo',
                                    sim.simx_opmode_streaming)
    
    time.sleep(0.1)

    destino_mundo = (0.5, 2.0)
    estado = IR_PARA_DESTINO
    direcao_contorno = None

    while True:
        err, data = sim.simxGetStringSignal(clientID, 
                                'Hokuyo',
                                sim.simx_opmode_buffer)
        _, pos = sim.simxGetObjectPosition(clientID,
                            robo_handle,
                            -1,
                            sim.simx_opmode_buffer)
        _, orient = sim.simxGetObjectOrientation(clientID,
                            robo_handle,
                            -1,
                            sim.simx_opmode_buffer)
        
        if err == sim.simx_return_ok and data:
            laser_data  = sim.simxUnpackFloats(data)
            start_angle = -120
            angle_step = 240 / len(laser_data)

            frente = []
            esquerda = []
            direita = []

            for i, dist in enumerate(laser_data):
                ang = start_angle + i * angle_step
                if -20 <= ang <= 20:
                    frente.append(dist)
                elif 45 <= ang <= 90:
                    esquerda.append(dist)
                elif -90 <= ang <= -45:
                    direita.append(dist)
                
            frente_livre = all(d > 0.5 for d in frente if d > 0.01)
            media_esq = np.mean([d for d in esquerda if d > 0.01]) if esquerda else 0
            media_dir = np.mean([d for d in direita if d > 0.01]) if direita else 0

            dx = destino_mundo[0] - pos[0]
            dy = destino_mundo[1] - pos[1]
            dist = math.hypot(dx, dy)
            ang_destino = math.atan2(dy, dx)
            erro = (ang_destino - orient[2] + math.pi) % ( 2 * math.pi) - math.pi

            if dist < 0.2:
                print("Destino alcançado")
                break

            if estado == IR_PARA_DESTINO:
                if frente_livre:
                    if abs(erro) > 1.0 and dist < 0.5:
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    -1.0 if erro<0 else 1.0,
                                                    sim.simx_opmode_streaming)
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    1.0 if erro<0 else -1.0,
                                                    sim.simx_opmode_streaming)
                    else:
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    2.0,
                                                    sim.simx_opmode_streaming)
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    2.0,
                                                    sim.simx_opmode_streaming)
                else:
                    direcao_contorno = ESQUERDA if media_esq > media_dir else DIREITA
                    estado = CONTORNAR_OBSTACULO

            elif estado == CONTORNAR_OBSTACULO:
                if frente_livre and abs(erro) < 1.0:
                    estado = IR_PARA_DESTINO
                else:
                    if direcao_contorno == DIREITA:
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    1.0,
                                                    sim.simx_opmode_streaming)
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    -0.5,
                                                    sim.simx_opmode_streaming)
                    else:
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    -0.5,
                                                    sim.simx_opmode_streaming)
                        sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    1.0,
                                                    sim.simx_opmode_streaming)
        time.sleep(0.1)
    
    sim.simxSetJointTargetVelocity(clientID, 
                                                    left_motor, 
                                                    0,
                                                    sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID, 
                                                    right_motor, 
                                                    0,
                                                    sim.simx_opmode_streaming)
    sim.simxFinish(clientID)
