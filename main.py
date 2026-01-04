import pygame
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize game window, etc
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def new(self):
        # Start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Create some platforms
        p1 = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40) # Floor
        p2 = Platform(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4, 100, 20)
        p3 = Platform(125, SCREEN_HEIGHT - 350, 100, 20)
        p4 = Platform(350, 200, 100, 20)
        
        self.platforms.add(p1, p2, p3, p4)
        self.all_sprites.add(p1, p2, p3, p4)
        
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # Check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.rect.midbottom = self.player.pos

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.jump()
                if event.key == pygame.K_q:
                     if self.playing:
                        self.playing = False
                     # Do not set running to False here, so we go to Game Over screen

    def draw(self):
        """
        Render the game state to the screen.
        """
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display to show the new frame
        pygame.display.flip()

    def show_start_screen(self):
        """Show the game splash/start screen."""
        self.screen.fill(BLACK)
        try:
            # Load and scale logo
            logo_img = pygame.image.load('logo.png')
            # detailed logo might need scaling, let's keep it reasonable width
            logo_img = pygame.transform.scale(logo_img, (400, 300))
            logo_rect = logo_img.get_rect()
            logo_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            
            # Fade-in animation
            for alpha in range(0, 256, 5): # Increment alpha
                self.clock.tick(FPS)
                self.screen.fill(BLACK)
                logo_img.set_alpha(alpha)
                self.screen.blit(logo_img, logo_rect)
                pygame.display.flip()
                
                # Check for quit during fade
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        self.running = False
                        return 

            # Keep the fully visible logo
            self.screen.blit(logo_img, logo_rect)
            pygame.display.flip()
            
            # Wait for 3 seconds
            self.wait_for_duration(SCREEN_DELAY)

        except pygame.error:
            # Fallback if image fails
            self.draw_text(SCREEN_TITLE, 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3)
        self.draw_text("Press a key to play", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        self.draw_text("Press Q to Quit", 18, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8)
        self.draw_text(VERSION, 12, WHITE, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10, align="bottomright")
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """Show the game over/continue screen."""
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        pygame.display.flip()

        # Wait for delay before showing restart instructions
        self.wait_for_duration(SCREEN_DELAY)
        self.draw_text("Press a key to play again or Q to quit", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()

        self.wait_for_key()

    def wait_for_duration(self, duration):
        """
        Wait for a specified duration in milliseconds.
        """
        start_wait = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_wait < duration:
            self.clock.tick(FPS)
            pygame.event.clear()

    def wait_for_key(self):
        """Wait for the user to press any key."""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        waiting = False
                        self.running = False
                    else:
                        waiting = False

    def draw_text(self, text, size, color, x, y, align="midtop"):
        """Helper to draw text on the screen."""
        font_name = pygame.font.match_font(FONT_NAME)
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        setattr(text_rect, align, (x, y))
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
sys.exit()
