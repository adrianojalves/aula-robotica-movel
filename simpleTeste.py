try:
    import sim
except:
    print("Erro o imortar biblioteca")

import time

sim.simxFinish(-1) #fecha conexões anteriores

clientID=sim.simxStart('127.0.0.1', 19999,True, True, 5000, 5)

if clientID != -1:
    print("conectou ao servidor")

    _, left_motor = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)#simx_opmode_blocking fica trvado até conectar
    _, right_motor = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)#simx_opmode_blocking fica trvado até conectar

    _, sensor5 = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor5', sim.simx_opmode_blocking)#simx_opmode_blocking fica trvado até conectar
    sim.simxReadProximitySensor(clientID, sensor5, sim.simx_opmode_streaming)

    def move_forward(speed=2.0, duration=0.5):
        sim.simxSetJointTargetVelocity(clientID, left_motor, speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, right_motor, speed, sim.simx_opmode_streaming)
        time.sleep(duration)

    def turn_left(speed=1.0, duration=1.0):
        sim.simxSetJointTargetVelocity(clientID, left_motor, -speed, sim.simx_opmode_streaming)
        sim.simxSetJointTargetVelocity(clientID, right_motor, speed, sim.simx_opmode_streaming)
        time.sleep(duration)

    def turn_right(speed=1.0, duration=1.0):
        sim.simxSetJointTargetVelocity(clientID, left_motor, speed, sim.simx_opmode_streaming)
        sim.simxS1etJointTargetVelocity(clientID, right_motor, -speed, sim.simx_opmode_streaming)
        time.sleep(duration)

    def stop():
        sim.simxSetJointTargetVelocity(clientID, left_motor, 0, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(clientID, right_motor, 0, sim.simx_opmode_blocking)

    start_time = time.time()
    while time.time() - start_time < 60:
        move_forward()
        _, detectionState, detectedPoint, _, _ = sim.simxReadProximitySensor(clientID, sensor5, sim.simx_opmode_buffer)
        print(detectionState)
        if detectionState:
            print(detectedPoint)
            x, y, z = detectedPoint
            if z < 0.9:
                turn_left()
        
        move_forward()
        time.sleep(1)

    stop()
else:
    print("NÃO conectou ao servidor")

print("programa finalizado")