try:
    import sim
except:
    print("Erro o imortar biblioteca")

import time
import numpy as np

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

    start_time = time.time()
    DURATION = 60 #60 segundos

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
                if -15 <= angle <= 15:
                    front_dist.append(dist)
                elif 45 <= angle <= 90:
                    left_dist.append(dist)
                elif -90 <= angle <= -45:
                    right_dist.append(dist)

            MIN_DISTANCE = 0.5

            obstacle_ahead = any(d < MIN_DISTANCE for d in front_dist)
            
            if obstacle_ahead:
                avg_left = np.mean(left_dist) if left_dist else 0
                avg_right = np.mean(right_dist) if right_dist else 0

                if avg_left > avg_right:
                    print("Girar para a esquerda")
                    sim.simxSetJointTargetVelocity(clientID, 
                                                left_motor, 
                                                -1.5,
                                                sim.simx_opmode_streaming)
                    sim.simxSetJointTargetVelocity(clientID, 
                                                right_motor, 
                                                1.5,
                                                sim.simx_opmode_streaming)
                else:
                    print("Girar para a direita")
                    sim.simxSetJointTargetVelocity(clientID, 
                                                left_motor, 
                                                1.5,
                                                sim.simx_opmode_streaming)
                    sim.simxSetJointTargetVelocity(clientID, 
                                                right_motor, 
                                                -1.5,
                                                sim.simx_opmode_streaming)
                
                time.sleep(1.2) #tempo de rotação
            else:
                sim.simxSetJointTargetVelocity(clientID, 
                                                left_motor, 
                                                2.0,
                                                sim.simx_opmode_streaming)
                sim.simxSetJointTargetVelocity(clientID, 
                                                right_motor, 
                                                2.0,
                                                sim.simx_opmode_streaming)

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