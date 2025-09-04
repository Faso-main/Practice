import requests
import time
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class BattleCityAIStrategy:
    def __init__(self, server_url):
        self.server_url = server_url
        self.session = requests.Session()
        self.team_id = None
        self.units = []
        self.map_width = 0
        self.map_height = 0
        self.current_tick = 0

    def connect(self, team_name):
        response = self.session.post(
            f"{self.server_url}/connect",
            json={"teamName": team_name}
        )
        data = response.json()
        self.team_id = data['teamId']
        self.map_width = data['world']['widthInBlocks']
        self.map_height = data['world']['heightInBlocks']
        self.units = data['world']['units']
        return data

    def get_world_state(self):
        response = self.session.get(
            f"{self.server_url}/world-state",
            params={"teamId": self.team_id}
        )
        data = response.json()
        self.current_tick = data['tick']
        return data

    def send_actions(self, actions):
        response = self.session.post(
            f"{self.server_url}/actions",
            json={
                "teamId": self.team_id,
                "tick": self.current_tick,
                "actions": actions
            }
        )
        return response.json()

    def make_decision(self, world_state):
        actions = []
        
        for unit in world_state['units']:
            if unit['teamId'] != self.team_id:
                continue
                
            action = {
                "unitId": unit['id'],
                "rotateTo": Direction.RIGHT.value,
                "moveAfterRotate": True,
                "shootAfterMove": False
            }
            
            if unit['canShoot'] and self.current_tick % 20 == 0:
                action["shootAfterMove"] = True
            
            actions.append(action)
        
        return actions

    def run(self):
        print("Connecting to server...")
        self.connect("PythonStrategy")
        
        while True:
            try:
                world_state = self.get_world_state()
                
                if world_state.get('gameOver', False):
                    print("Game over! Winner:", world_state.get('winner'))
                    break
                
                actions = self.make_decision(world_state)
                self.send_actions(actions)
                
                time.sleep(0.1) 
                
            except Exception as e:
                print("Error:", e)
                break

if __name__ == "__main__":
    SERVER_URL = "http://localhost:6469"
    
    strategy = BattleCityAIStrategy(SERVER_URL)
    strategy.run()