import random
import pygame
from PIL import Image, ImageDraw
import os
import math

main_dir = os.path.split(os.path.abspath(__file__))[0]
asset_dir = os.path.join(main_dir, "assets")
# pygame setup
pygame.init()
WIDTH, HEIGHT = 500, 500

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(asset_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = load_image('undersea.png')[0].convert()
mer = background.subsurface(pygame.Rect(background.get_width()//2, 650, background.get_width()//2, background.get_height()//4))
player = load_image('Boat.png')[0].convert_alpha()
icon = load_image('Icons_01.png')[0].convert_alpha()
clock = pygame.time.Clock()
running = True


pygame.display.set_icon(icon)

def create_fish_image():
    """return image pgame"""
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fish body (ellipse shape)
    body_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.ellipse((5, 8, 27, 24), fill=body_color)
    
    # triangle
    draw.polygon([(5, 16), (0, 10), (0, 22)], fill=body_color)
    
    # Fish eye
    draw.ellipse((20, 12, 24, 16), fill=(255, 255, 255))
    draw.ellipse((22, 13, 23, 15), fill=(0, 0, 0))
    
    # Convert PIL Image to Pygame Surface
    mode = img.mode
    size = img.size
    data = img.tobytes()
    pygame_img = pygame.image.fromstring(data, size, mode)
    return pygame_img

class Fish:
    def __init__(self):
        self.image = create_fish_image()
        self.pos = self.image.get_rect()
        self.speed = random.uniform(1.5, 3.0)
        self.jump_speed = random.uniform(8, 12)
        self.gravity = 0.5
        self.jump_height = random.randint(30, 80)
        self.reset_position()
        
        # Jumping state
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_target_x = 0
        self.jump_target_y = 0
        self.original_y = 0
        self.jump_timer = 0
        self.max_jump_time = 60  # frames
        
    def reset_position(self):
        """Reset fish to starting position at water surface"""
        water_surface = HEIGHT - mer.get_height()
        self.pos.x = random.randint(0, WIDTH - self.pos.width)
        self.pos.y = water_surface - self.pos.height
        self.is_jumping = False
        self.jump_velocity = 0
        
    def start_jump(self, target_x, target_y):
        """Start a jump towards target position"""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_timer = 0
            self.original_y = self.pos.y
            self.jump_target_x = target_x
            self.jump_target_y = target_y
            
            # Calculate initial velocity for parabolic jump
            dx = target_x - self.pos.x
            dy = target_y - self.pos.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Adjust jump strength based on distance
            power = min(15, max(8, distance / 20))
            self.jump_velocity = -power
            
    def update(self, player_pos):
        """Update fish position and jumping state"""
        water_surface = HEIGHT - mer.get_height()
        
        if self.is_jumping:
            self.jump_timer += 1
            
            # Apply gravity
            self.jump_velocity += self.gravity
            self.pos.y += self.jump_velocity
            
            # Move horizontally towards target
            dx = self.jump_target_x - self.pos.x
            self.pos.x += dx * 0.05  # Horizontal movement speed
            
            # Check if jump is complete (hit water or timeout)
            if self.pos.y >= water_surface - self.pos.height:
                self.reset_position()
            elif self.jump_timer > self.max_jump_time:
                self.reset_position()
                
            # Small chance to randomly jump if near player
            if random.random() < 0.01:  # 1% chance per frame
                self.start_jump(player_pos.x, player_pos.y)
        else:
            # Swim slowly in water
            self.pos.x += random.uniform(-0.5, 0.5)
            
            # Keep fish in water bounds
            self.pos.x = max(0, min(WIDTH - self.pos.width, self.pos.x))
            self.pos.y = water_surface - self.pos.height + random.uniform(-2, 0)
            
            # Check if player is nearby to trigger jump
            player_center = pygame.Rect(player_pos.x, player_pos.y, 
                                       player_pos.width, player_pos.height).center
            fish_center = self.pos.center
            
            distance = math.sqrt((player_center[0] - fish_center[0])**2 + 
                               (player_center[1] - fish_center[1])**2)
            
            if distance < 100 :  
                self.start_jump(player_center[0], player_center[1])

class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(height, mer.get_height() + height)

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
        if self.pos.right < 0:
            self.pos.right = WIDTH

# Initialize game objects
joueur = GameObject(player, 10, 3)
fishes = [Fish() for _ in range(3)]  
last_fish_spawn = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Add more fish when space is pressed
                fishes.append(Fish())
    
    pygame.display.set_caption(f'Le jeu Incroyable d\'allan - FPS: {clock.get_fps():.2f} - Fish: {len(fishes)}')

    #background
    screen.fill((135, 206, 235))  
    screen.blit(mer, (0, HEIGHT - mer.get_height()))
    
    # Update and draw fishes
    for fish in fishes:
        fish.update(joueur.pos)
        screen.blit(fish.image, fish.pos)
    
    # Draw player
    screen.blit(joueur.image, (joueur.pos.left, joueur.pos.top))
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        joueur.move(left=True)
    if keys[pygame.K_RIGHT]:
        joueur.move(right=True)
    
    # Remove fish that are too far off screen
    fishes = [fish for fish in fishes if fish.pos.x > -100 and fish.pos.x < WIDTH + 100]
    
    # Flip the display
    pygame.display.flip()
    
    # Limits FPS to 60
    clock.tick(60)

pygame.quit()