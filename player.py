import pygame
import config
from math import floor

class Player:
    
    # left, right, up, down
    direction = [0, 0, 0, 0]
    
    #width, height
    size = (20, 20)
    
    # upleft, upright, downleft, downright
    edges = {'ul': [0, 0], 'ur': [0, 0], 'dl': [0, 0], 'dr': [0, 0], 'xline': [], 'yline': []};
    
    xline = []
    yline = []
    
    def __init__(self, screen, window_size):
        self.cfg = config.Config(file('config.ini'))
        self.screen = screen
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 4
        self.position = (self.x, self.y)
        self.speed = self.stop()
        self.moving_speed = self.cfg.init_player_speed
        self.window_size = window_size

    def draw(self):
        self.update_position()
        rect = (self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 0)
        self.__draw_players_eye()

    def __draw_players_eye(self):
        eye_size = 6
        #left
        if self.direction[0]:
            rect = [self.x + 2, self.y + self.size[1] / 2 - eye_size / 2]
        #right
        elif self.direction[1]:
            rect = [self.x + self.size[0] - 2 - eye_size, self.y + self.size[1] / 2 - eye_size / 2]
        #up
        elif self.direction[2]:
            rect = [self.x + self.size[0] / 2 - eye_size / 2, self.y + 2]
        #down
        elif self.direction[3]:
            rect = [self.x + self.size[0] / 2 - eye_size / 2, self.y + self.size[1] - 2 - eye_size]
        else:
            rect = [self.x + self.size[0] / 2 - eye_size / 2, self.y + self.size[1] / 2 - eye_size / 2]
        rect.append(eye_size)
        rect.append(eye_size)
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 0)
        
    def update_position(self):
        if self.direction[0]:
            self.x -= self.speed
        if self.direction[1]:
            self.x += self.speed
        if self.direction[2]:
            self.y -= self.speed
        if self.direction[3]:
            self.y += self.speed
        self.position = (self.x, self.y)
        self.__check_borders()
        self.__get_edge_points()
    
    def __check_borders(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > self.screen.get_width() - self.size[0]:
            self.x = self.screen.get_width() - self.size[0]
        if self.y > self.screen.get_height() - self.size[1]:
            self.y = self.screen.get_height() - self.size[1]

    def __get_edge_points(self):
        self.edges['ul'] = [self.x, self.y]
        self.edges['ur'] = [self.x + self.size[0], self.y]
        self.edges['dl'] = [self.x, self.y + self.size[1]]
        self.edges['dr'] = [self.x + self.size[0], self.y + self.size[1]]
        self.xline = range(self.edges['ul'][0], self.edges['ur'][0] + 1)
        self.yline = range(self.edges['ul'][1], self.edges['dl'][1] + 1)

    def left(self):
        self.direction[0] = 1
        
    def right(self):
        self.direction[1] = 1
        
    def up(self):
        self.direction[2] = 1
        
    def down(self):
        self.direction[3] = 1
        
    def start(self):
        self.speed = self.moving_speed
        
    def stop(self):
        for i in range(0, 4):
            self.direction[i] = 0
        self.speed = 0
        
    def hit_obstacle(self, obstacles):
        for obstacle in obstacles:
            oe = obstacle.edges
            xline = range(oe['ul'][0], oe['ur'][0] + 1)
            yline = range(oe['ul'][1], oe['dl'][1] + 1)
            if bool(set(xline) & set(self.xline)) and bool(set(yline) & set(self.yline)):
                return True
        return False
    
    def mouse_move(self):
        if pygame.mouse.get_focused():
            self.x = pygame.mouse.get_pos()[0]
            self.y = pygame.mouse.get_pos()[1]
            
    def keyboard_move(self, event):
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                self.stop()

        if event.type == pygame.KEYDOWN:
            self.start()
            if event.key == pygame.K_LEFT:
                self.left()
            if event.key == pygame.K_RIGHT:
                self.right()
            if event.key == pygame.K_UP:
                self.up()
            if event.key == pygame.K_DOWN:
                self.down()

            