from obstacle import Obstacle

class Obstacles:
    
    collection = []
    
    def __init__(self, screen, window_size):
        self.screen = screen
        self.window_size = window_size
    
    def gen_obstacles(self, total = 30):
        while True:
            if total == 0:
                break
            self.add()
            total -= 1
    def up(self, speed):
        for obstacle in self.collection:
            obstacle.up(speed)
            
    def draw(self):
        for obstacle in self.collection:
            obstacle.draw()
    
    def add(self):
        obstacle = Obstacle(self.screen, self.window_size)
        obstacle.gen_random_parameters_from_bottom()
        self.collection.append(obstacle)
        
    def one_more(self):
        self.add()