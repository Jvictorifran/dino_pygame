import pygame 
from pygame.locals import *
from sys import exit
import os
from random import randrange

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

#definindo os tamanhos da janela
LARGURA = 640
ALTURA = 480

#cores 
BRANCO = (255,255,255)

#vairaveis da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Dino")

#classes, variaveis e sprites
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, "dinoSpritesheet.png")).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))

colidiu = False
#classe do dinossauro
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.image_dinossauro = []
        for i in range(3):
            img =  sprite_sheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.image_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.image_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(img)
        self.pos_y_inicial = ALTURA - 64 - 96//2
        self.rect.center = (100, ALTURA - 64)
        self.pulo = False

    #metodo de update da classe dino
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.image_dinossauro[int(self.index_lista)]
    #metodo de pular da classe dino
    def pular(self):
        self.pulo = True
        self.som_pulo.play()

#classe das nuvens
class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA- randrange(30, 300, 90)
    
    #metodo de update da classe nuvem
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA 
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10

#classe do chão 
class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64

    #update da classe chao
    def update (self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA 
        self.rect.x -= 10
    
#classe cacto
class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))  
        self.rect = self.image.get_rect() 
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (LARGURA, ALTURA-64)

    #update da classe cacto
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        else:
            self.rect.x -=10

#aqui ficam todas as sprites do jogo
todas_as_sprites = pygame.sprite.Group()

#armazenamento ca classe dino
dino = Dino()
todas_as_sprites.add(dino)

#armazenamento do objeto nuvem
for i in range(4):  
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

#armazenamento do objeto chao
for i in range(20):
    chao = Chao(i)
    todas_as_sprites.add(chao)

#armazenamento do objeto cacto
cacto = Cacto()
todas_as_sprites.add(cacto)

#grupo dos obsctaculos
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)

#fps 
relogio = pygame.time.Clock()

# loop principal do jogo
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)
    todas_as_sprites.draw(tela)

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True
        
    if colidiu == True:
        pass
    
    else:
        todas_as_sprites.update()

    pygame.display.flip()