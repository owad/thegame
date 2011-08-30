#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
import time
import csv
import operator
import config
from player import Player
from background import Background 
from obstacles import Obstacles


class Game:
    
    def __init__(self):
        self.cfg = config.Config(file('config.ini'))
        self.game_start_time = time.time()
        self.game_speed = self.cfg.init_game_speed
        self.play_time = 0
        self.game_score = 0
        self.player_name = ''
        
        self.fps = self.cfg.fps
        pygame.init()
        try:
            if sys.argv[1] == 'fullscreen':
                info = pygame.display.Info()
                self.window_size = (info.current_w, info.current_h)
                pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
        except:
            self.window_size = (640, 480)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        
        self.obstacles = Obstacles(self.screen, self.window_size)
        self.obstacles.gen_obstacles(1)
        self.player = Player(self.screen, self.window_size)
        self.bg = Background(self.screen)
    
    def display_text(self, text, x=None, y=None, font_size=40):
        myfont = pygame.font.SysFont("Arial Bold", font_size)
        label = myfont.render(text, 1, (255, 255, 255))
        if not x:
            x = self.window_size[0] / 2 - label.get_width() / 2
        if not y:
            y = self.window_size[1] / 3
        self.screen.blit(label, (x, y))
        return label

    def game_over(self):
        self.display_text('GAME OVER', None, 50)
        self.display_text("your score is %s" % self.game_score, None, 80)
        
    def game_score_display(self):
        self.play_time = time.time() - self.game_start_time
        self.display_text("Score: %s" % str(self.game_score), 10, 10)
    
    def game_score_save(self, key_index=None):
        if len(self.player_name) < 3:
            if key_index != None and key_index > 96 and key_index < 123:
                self.player_name += chr(key_index)
            self.display_text('Type your initials: %s' % self.player_name, None, 120, 30)
        elif len(self.player_name) == 3:
            writer = csv.writer(open('scores.txt', 'ab'))
            writer.writerow([self.player_name, self.game_score])
            self.player_name += '-1'
        elif int(self.player_name[-1:]) == 1:
            self.player_name = 'abc2'
            reader = csv.reader(open('scores.txt', 'rb'))
            scores = []
            for row in reader:
                scores.append((row[0], row[1]))
            scores.sort(None, operator.itemgetter(1), True)
            writer = csv.writer(open('scores.txt', 'wb'))
            writer.writerows(scores[:5])
        else:
            self.game_score_board()
            
    def game_score_board(self):
        reader = csv.reader(open('scores.txt', 'rb'))
        y = 120
        self.display_text("Top scores", None, y, 30)
        y = 150
        for row in reader:
            self.display_text('%s %s' % (row[0].upper(), row[1]), None, y, 30)
            y += 30
    
    def game_speedup(self, speedup=1):
        self.game_speed += speedup
    
    def draw(self, hide_scores=False):
        self.bg.draw()
        self.obstacles.draw()
        self.player.draw()
        if not hide_scores:
            self.game_score_display()
    
    def main(self):
        done = False
        stop = False
        gameover = False
        speedup_counter = self.fps
        while done == False:
            if not gameover:
                if self.player.hit_obstacle(self.obstacles.collection):
                    gameover = True
            key_index = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if gameover:
                        key_index = event.key
                self.player.keyboard_move(event)
            self.player.mouse_move()
            
            self.obstacles.up(self.game_speed)
            if speedup_counter > 0:
                speedup_counter -= 1
            else:
                if int(self.play_time) % 5 == 0 and self.play_time != 0:
                    self.game_speedup()
                    if len(self.obstacles.collection) < self.cfg.max_obstacles:
                        self.obstacles.one_more()
                speedup_counter = self.fps
            if not stop:
                self.clock.tick(self.fps)
            
            self.draw(gameover)
            
            if gameover:
                self.game_over()
                self.game_score_save(key_index)
                stop = True
            else: 
                self.game_score += 1
            
            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.main()
    pygame.quit()
