import pygame
from PIL import Image, ImageDraw

# pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
objects = []
background = pygame.image.load('fishing_game_assets/3 Objects/undersea.png').convert()
partie_decoupee = background.subsurface(pygame.Rect(background.get_width()//2, 550, background.get_width()//2, background.get_height()//4))
player = pygame.image.load('fishing_game_assets/3 Objects/Boat.png').convert()


def getPoisson():
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed
        if self.pos.right > WIDTH:
            self.pos.left = 0
        if self.pos.top > HEIGHT-self.image.get_height():
            self.pos.top = 0
        if self.pos.right < self.image.get_width():
            self.pos.right = WIDTH
        if self.pos.top < 0:
            self.pos.top = HEIGHT-self.image.get_height()



joueur = GameObject(player, 10, 3) 

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.set_caption('Le jeu Incroyable d\'allan')



    screen.blit(partie_decoupee, (0, 0))
    screen.blit(joueur.image, (joueur.pos.left, joueur.pos.top))
    
    
    keys = pygame.key.get_pressed()
    # mouvement du joueur 200 pixels per second
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        joueur.move(up=True)
    if keys[pygame.K_DOWN]:
        joueur.move(down=True)
    if keys[pygame.K_LEFT]:
        joueur.move(left=True)
    if keys[pygame.K_RIGHT]:
        joueur.move(right=True)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    pygame.display.update()
    clock.tick(60)

pygame.quit()