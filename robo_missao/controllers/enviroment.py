import sim

class Enviroment:
    clientID = None
    
    def get_client_id(self):
        if self.clientID is None:
            print('Conectando ao CoppeliaSim...')
            sim.simxFinish(-1)
            self.clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
            return self.clientID
        return None
    
    def encerrar_simulacao(self):
        sim.simxFinish(self.clientID)
