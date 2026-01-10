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
        self.player_color = YELLOW
        self.last_platform = None

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        self.player = Player(self, self.player_color)
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
        # Place directly on top to prevent "falling" logic from triggering score on spawn
        self.player.pos = pygame.math.Vector2(p_start.rect.centerx, p_start.rect.top)
        self.last_platform = p_start
        
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
                # AND if we land on a different platform
                if self.player.vel.y > PLAYER_GRAVITY:
                    if hits[0] != self.last_platform:
                        self.score += SCORE_PER_PLATFORM
                        self.last_platform = hits[0]

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
        
        # Draw current score in player's color
        self.draw_text(str(self.score), 22, self.player_color, SCREEN_WIDTH / 2, 15)
        
        # Draw all-time high score in player's color
        if self.hs_manager.scores:
            top_score = self.hs_manager.scores[0]
            hs_color = top_score.get('color', YELLOW)
            if isinstance(hs_color, list): hs_color = tuple(hs_color)
            self.draw_text(f"HS: {top_score['score']}", 22, hs_color, SCREEN_WIDTH - 10, 15, align="topright")
        
        # *after* drawing everything, flip the display to show the new frame
        pygame.display.flip()

    def show_start_screen(self):
        """Show the game splash/start screen."""
        self.screen.fill(BLACK)
        try:
            # Load and scale logo
            # Load and scale logo
            logo_img = pygame.image.load('logo.png')
            
            # User scaling request: fit to screen keeping aspect ratio
            # Determine scale factor
            l_rect = logo_img.get_rect()
            scale_w = SCREEN_WIDTH / l_rect.width
            scale_h = SCREEN_HEIGHT / l_rect.height
            scale = min(scale_w, scale_h)
            
            new_size = (int(l_rect.width * scale), int(l_rect.height * scale))
            logo_img = pygame.transform.scale(logo_img, new_size)
            
            logo_rect = logo_img.get_rect()
            logo_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            
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
                        
            # Keep the fully visible logo for a moment
            self.screen.blit(logo_img, logo_rect)
            pygame.display.flip()
            self.wait_for_duration(SCREEN_DELAY)

        except pygame.error:
            pass # Fallback if image fails

        self.show_color_selection_screen()

    def show_color_selection_screen(self):
        """Show value selection screen."""
        # Check if user wants to play again (loop handled by main block)
        # But we need to wait here for a key press
        self.screen.fill(BLACK)
        self.draw_text(SCREEN_TITLE, 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 5)
        
        # Determine color name string
        c_name = "Yellow"
        if self.player_color == RED: c_name = "Red"
        elif self.player_color == BLUE: c_name = "Blue"
        
        self.draw_text(f"Current Player Color: {c_name}", 22, self.player_color, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Press (R)ed, (B)lue, (Y)ellow to select", 18, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30)
        self.draw_text("Press ENTER to play", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        
        # Draw version
        self.draw_text(f"v{VERSION}", 16, WHITE, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 20)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    # 'Q' to quit
                    if event.key == pygame.K_q:
                        waiting = False
                        self.running = False
                    # Color selection
                    elif event.key == pygame.K_r:
                        self.player_color = RED
                        self.show_color_selection_screen() # Refresh
                        return # Break this call, let the refreshed call handle loop
                    elif event.key == pygame.K_b:
                        self.player_color = BLUE
                        self.show_color_selection_screen()
                        return
                    elif event.key == pygame.K_y:
                        self.player_color = YELLOW
                        self.show_color_selection_screen()
                        return
                    # Start
                    elif event.key == pygame.K_RETURN:
                        waiting = False

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
        self.draw_text("Score: " + str(self.score), 22, self.player_color, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        
        # Show High Scores
        self.draw_text("HIGH SCORES", 28, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
        y_pos = SCREEN_HEIGHT / 2
        for i, entry in enumerate(self.hs_manager.scores):
            entry_color = entry.get('color', YELLOW)
            # Ensure color is a tuple/list, sometimes json loads as list
            if isinstance(entry_color, list):
                entry_color = tuple(entry_color)
                
            text = f"{entry['name']}   {entry['score']}"
            self.draw_text(text, 22, entry_color, SCREEN_WIDTH / 2, y_pos)
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
            self.draw_text("Press Enter to Submit", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(name) > 0: # Force at least 1 char? Optional.
                            self.hs_manager.add_score(name, self.score, self.player_color)
                            waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 3 and event.unicode.isalpha():
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
