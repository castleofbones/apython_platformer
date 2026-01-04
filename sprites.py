import pygame

# Player constants
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Ensure we have a surface; fill it with a distinct color (e.g., Yellow)
        self.image = pygame.Surface((30, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        
        # Position and velocity
        self.pos = pygame.math.Vector2(10, 385)  # Start above the ground
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def jump(self):
        # Jump only if standing on a platform
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the screen (optional, maybe remove later if we want strict bounds)
        if self.pos.x > self.game.screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.game.screen_width

        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
