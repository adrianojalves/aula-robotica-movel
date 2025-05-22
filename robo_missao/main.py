from controllers.robot_controller import RobotController
from controllers.enviroment import Enviroment
from services.mission_manager import MissionManager

def main():
    enviroment = Enviroment()
    clientID = enviroment.get_client_id()
    print(clientID)
    if clientID != None and clientID != -1:
        print('Conectado com sucesso!')
        
        robot_ctrl = RobotController(clientID)
        mission = MissionManager(robot_ctrl)
        mission.executar()

        enviroment.encerrar_simulacao()
    else:
        print("Erro ao conectar ao CoppeliaSim.")

if __name__ == "__main__":
    main()