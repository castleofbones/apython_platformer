import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, color=YELLOW):
        super().__init__()
        self.game = game
        self.player_color = color
        self.load_images()
        
        self.image = self.standing_frame
        self.rect = self.image.get_rect()
        
        # Position and velocity
        # 'pos' tracks exact float position for physics, 'rect' tracks integer position for drawing
        self.pos = pygame.math.Vector2(10, 385)  # Start above the ground
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

    def load_images(self):
        self.standing_frame = self.get_image('p1_idle.png')
        self.walk_frames_r = [self.get_image('p1_walk1.png'), self.get_image('p1_walk2.png')]
        self.walk_frames_l = [pygame.transform.flip(frame, True, False) for frame in self.walk_frames_r]
        self.jump_frame = self.get_image('p1_jump.png')
        
    def get_image(self, filename):
        img_path = os.path.join('images', filename)
        try:
            image = pygame.image.load(img_path).convert_alpha()
        except pygame.error:
             # Fallback if image missing - create colored block
            image = pygame.Surface((30, 40))
            image.fill(WHITE)

        # Tint the image with the player's color
        # We can use BLEND_MULT or BLEND_RGBA_MULT if using alpha
        # Simple approach: Create a surface of same size, fill with color, blend
        tint_surf = pygame.Surface(image.get_size()).convert_alpha()
        tint_surf.fill(self.player_color)
        image.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_MULT)
        
        return image

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
        self.animate()
        
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

    def animate(self):
        now = pygame.time.get_ticks()
        
        # Check if we are walking
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
            
        # Check if jumping (in air)
        # Simple check: if vertical velocity is significant
        if abs(self.vel.y) > 0.5: # small threshold
            self.jumping = True
        else:
            self.jumping = False

        # Show Jump Frame
        if self.jumping:
            self.image = self.jump_frame
            # Flip based on direction
            if self.vel.x < 0:
                self.image = pygame.transform.flip(self.jump_frame, True, False)
        
        # Show Walk Animation
        elif self.walking:
            if now - self.last_update > 200: # 200ms per frame
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    
        # Show Idle Frame
        if not self.jumping and not self.walking:
            self.image = self.standing_frame

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
