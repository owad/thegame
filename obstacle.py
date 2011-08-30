import pygame
from random import choice 

class Obstacle:
    
    x = None
    y = None
    color = None
    width = None
    
    # upleft, upright, downleft, downright
    edges = None
    
    window_size = None
    
    def __init__(self, screen, window_size):
        self.screen = screen
        self.window_size = window_size
        self.edges = {'ul': [0, 0], 'ur': [0, 0], 'dl': [0, 0], 'dr': [0, 0]};
        
    def draw(self):
        self.__get_edge_points()
        if self.is_gone():
            self.gen_random_parameters_from_bottom()
        self.draw_square()

    def draw_square(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.width))

    def gen_random_parameters(self):
        self.x = self.__gen_random_x()
        self.y = self.__gen_random_y()
        self.color = self.__gen_random_color()
        self.width = self.__gen_random_width()
        
    def gen_random_parameters_from_bottom(self):
        self.gen_random_parameters()
        self.y = self.window_size[1]

    def up(self, speed):
        self.y -= speed
    
    def __get_edge_points(self):
        self.edges['ul'] = [self.x, self.y]
        self.edges['ur'] = [self.x + self.width, self.y]
        self.edges['dl'] = [self.x, self.y + self.width]
        self.edges['dr'] = [self.x + self.width, self.y + self.width]
    
    def __gen_random_x(self):
        return choice(range(self.window_size[0]))
    
    def __gen_random_y(self):
        return choice(range(self.window_size[1]))
    
    def __gen_random_width(self, min=5, max=35):
        return choice(range(min, max))
    
    def __gen_random_color(self):
        return (choice(range(256)), choice(range(256)), choice(range(256)))
    
    def is_gone(self):
        if self.y < 0:
            return True
        else:
            return False