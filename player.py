import pygame

class Player():
    def __init__(self, gridsize):
        self.x = gridsize * 2
        self.y = gridsize * 2
        self.direction = 0.001
        self.vrot = 0
        self.speed = .1
        self.turnSpeed = .001
        self.size = gridsize
        self.height = 0
    
    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x - self.size/2, self.y - self.size/2, self.size, self.size))
