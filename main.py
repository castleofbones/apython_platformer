import pygame
import sys
from settings import *
from sprites import *
from highscore_manager import HighScoreManager

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
        self.hs_manager = HighScoreManager()

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Create some platforms
        p1 = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, is_floor=True) # Floor
        
        # Starting platform near left, just above lava
        p_start = Platform(50, SCREEN_HEIGHT - 120, 150, 20)
        
        p2 = Platform(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4, 100, 20)
        p3 = Platform(125, SCREEN_HEIGHT - 350, 100, 20, moving=True)
        p4 = Platform(350, 200, 100, 20)
        
        self.platforms.add(p1, p_start, p2, p3, p4)
        self.all_sprites.add(p1, p_start, p2, p3, p4)
        
        # Set player position to start on the safe platform
        self.player.pos = pygame.math.Vector2(p_start.rect.centerx, p_start.rect.top - 40)
        
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
                # Check for floor (Game Over)
                if getattr(hits[0], 'is_floor', False):
                    self.playing = False
                    return

                self.player.pos.y = hits[0].rect.top
                
                # Only score if we were actually falling (more than just gravity adjustment)
                # Gravity adds 0.8 per frame, so standing still creates 0.8 velocity.
                # Falling from a jump or drop will have higher velocity.
                if self.player.vel.y > PLAYER_GRAVITY:
                    self.score += SCORE_PER_PLATFORM

                self.player.vel.y = 0
                
                # If platform is moving, move player with it
                if getattr(hits[0], 'moving', False):
                    self.player.pos.x += hits[0].velocity
                
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
        self.draw_text(str(self.score), 22, WHITE, SCREEN_WIDTH / 2, 15)
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
        """
        Show the game over screen.
        Checks for high scores, handles name input if applicable,
        and displays the high score leaderboard.
        """
        if not self.running:
            return
            
        # Check for high score
        if self.hs_manager.is_high_score(self.score):
            self.get_high_score_name()
            
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6)
        self.draw_text("Score: " + str(self.score), 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        
        # Show High Scores
        self.draw_text("HIGH SCORES", 28, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
        y_pos = SCREEN_HEIGHT / 2
        for i, entry in enumerate(self.hs_manager.scores):
            text = f"{entry['name']}   {entry['score']}"
            self.draw_text(text, 22, WHITE, SCREEN_WIDTH / 2, y_pos)
            y_pos += 30

        # Wait for delay before showing restart instructions
        self.wait_for_duration(SCREEN_DELAY)
        self.draw_text("Press a key to play again or Q to quit", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8)
        pygame.display.flip()

        self.wait_for_key()

    def get_high_score_name(self):
        """
        Input loop for getting the user's initials (3 characters).
        Updates the high score manager with the new entry.
        """
        name = ""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            self.draw_text("NEW HIGH SCORE!", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            self.draw_text("Enter Initials: " + name, 36, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(name) > 0: # Force at least 1 char? Optional.
                            self.hs_manager.add_score(name, self.score)
                            waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 3 and event.unicode.isalnum():
                            name += event.unicode.upper()

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

if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pygame.quit()
    sys.exit()
