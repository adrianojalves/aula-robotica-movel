import sim
import time
import sys

print('Conectando ao CoppeliaSim...')

sim.simxFinish(-1)  # Fecha conexões antigas
client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if client_id != -1:
    print('Conectado ao CoppeliaSim com sucesso!')

    # Obtém os handles das rodas
    _, rear_left = sim.simxGetObjectHandle(client_id, 'joint_back_left_wheel', sim.simx_opmode_blocking)
    _, rear_right = sim.simxGetObjectHandle(client_id, 'joint_back_right_wheel', sim.simx_opmode_blocking)
    _, front_left = sim.simxGetObjectHandle(client_id, 'joint_front_left_wheel', sim.simx_opmode_blocking)
    _, front_right = sim.simxGetObjectHandle(client_id, 'joint_front_right_wheel', sim.simx_opmode_blocking)

    # Define a velocidade desejada para cada roda
    speed = 2.0  # rad/s

    sim.simxSetJointTargetVelocity(client_id, front_left, -speed, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_id, front_right, speed, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_id, rear_right, speed, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_id, rear_left, -speed, sim.simx_opmode_streaming)

    # Aguarda 5 segundos
    time.sleep(25)

    # Para o robô
    sim.simxSetJointTargetVelocity(client_id, front_left, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client_id, front_right, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client_id, rear_right, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client_id, rear_left, 0, sim.simx_opmode_oneshot)

    # Fecha a conexão
    sim.simxFinish(client_id)

else:
    print('Falha ao conectar. Verifique se o CoppeliaSim está rodando com o Remote API ativo.')
    sys.exit()
