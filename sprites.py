import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, color=YELLOW):
        super().__init__()
        self.game = game
        # Ensure we have a surface; fill it with a distinct color (e.g., Yellow)
        self.image = pygame.Surface((30, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        # Position and velocity
        # 'pos' tracks exact float position for physics, 'rect' tracks integer position for drawing
        self.pos = pygame.math.Vector2(10, 385)  # Start above the ground
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def jump(self):
        """
        Make the player jump if they are standing on a platform.
        """
        # Look 1 pixel down to see if there is a platform
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        
        # If we hit something below, we can jump
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        """
        Update the player's position based on inputs and physics.
        """
        # Apply Gravity constantly
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        
        # Check keys for horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply friction to Acc ( Friction * Velocity )
        # This creates a max speed and slows player down when input releases
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Physics Equations of Motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the screen (teleport to other side)
        if self.pos.x > self.game.screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.game.screen_width

        # Update the rectangle position (for drawing collisions)
        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    """
    Represents static level geometry that the player can stand on.
    """
    def __init__(self, x, y, w, h, moving=False, is_floor=False):
        super().__init__()
        self.image = pygame.Surface((w, h))
        if is_floor:
            self.image.fill(RED)
        else:
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_floor = is_floor
        
        self.moving = moving
        if self.moving:
            self.start_x = x
            # Distance to travel is equal to width. 
            # Speed = Distance / Time (in frames approx, or pixels per update)
            # Duration is in ms. Updates per second is FPS.
            # Total frames = (Duration / 1000) * FPS
            # Speed = Width / Total frames
            total_frames = (PLATFORM_MOVE_DURATION / 1000) * FPS
            self.velocity = w / total_frames
            
    def update(self):
        if self.moving:
            self.rect.x += self.velocity
            
            # Check bounds (move right by width, so range is [start_x, start_x + width])
            if self.rect.x > self.start_x + self.rect.width:
                self.velocity = -abs(self.velocity)
            if self.rect.x < self.start_x:
                self.velocity = abs(self.velocity)
