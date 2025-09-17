import pygame 
from pygame.locals import *
from sys import exit
import os

diretorio_principal = os.path.dirname(__file__)

#definindo os tamanhos da janela
LARGURA = 640
ALTURA = 480

#cores 
BRANCO = (255,255,255)

#vairaveis da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set__caption("Jogo do Dino")

#classes, variaveis e sprites
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass

todas_as_sprites = pygame.sprite.Group
dino = Dino()
todas_as_sprites.add(dino)

relogio = pygame.time.Clock()

# loop principal do jogo
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
