try:
    import sim
except:
    print("Erro o imortar biblioteca")

import time
import math
import matplotlib.pyplot as plt

sim.simxFinish(-1) #fecha conexões anteriores

clientID=sim.simxStart('127.0.0.1', 19999,True, True, 5000, 5)

if clientID != -1:
    print("conectou ao servidor")

    err, data = sim.simxGetStringSignal(clientID, 'Hokuyo', sim.simx_opmode_blocking)

    if err == sim.simx_return_ok and data:
        laser_data = sim.simxUnpackFloats(data)

        num_reading = len(laser_data)
        if num_reading == 0:
            print("Nenhum dado recebido")
            sim.simxFinish(-1)
            exit()
        
        #por padrão o fasthokuyo cobre 240º
        #de -120 a 120
        start_angle = -120
        end_angle = 120
        angle_step = 240 / num_reading

        x_coords = []
        y_coords = []

        for i, distance in enumerate(laser_data):
            #primeiro converter o angulo para radiano
            angle = math.radians(start_angle + i * angle_step)
            #achar coordenadas x e y a partir do sen e cos
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)

            x_coords.append(x)
            y_coords.append(y)
        
        plt.figure(figsize=(6,6), dpi=100)
        plt.scatter(x_coords, y_coords, c='r', marker='o', label="Pontos detectados")
        plt.plot(0,0, 'k>', markersize=10, label="Robô")

        plt.xlim([-5.5, 5.5])
        plt.ylim([-5.5, 5.5])
        plt.grid()
        plt.xlabel("X (metros)")
        plt.ylabel("Y (metros)")
        plt.title("Mapa do ambiente detectado")
        plt.legend()
        plt.show()
    else:
        print("Erro ao obter dados do laser")

    sim.simxFinish(-1)

print("Programa finalizdo")