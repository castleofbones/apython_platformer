import pytest
import pygame
from unittest.mock import MagicMock
from main import Game
from sprites import Platform
from settings import *

@pytest.fixture
def game():
    g = Game()
    g.run = MagicMock() # Block run
    g.score = 0
    return g

def test_score_increment(game):
    game.new()
    game.platforms.empty()
    
    # Normal platform
    plat = Platform(0, 300, 100, 20, is_floor=False)
    game.platforms.add(plat)
    
    # Falling player hitting platform
    game.player.pos = pygame.math.Vector2(50, 290)
    game.player.vel.y = 10
    
    game.update()
    
    assert game.score == SCORE_PER_PLATFORM
    assert game.player.vel.y == 0

def test_game_over_on_floor(game):
    game.new()
    game.platforms.empty()
    
    # Floor platform
    floor = Platform(0, 500, 800, 40, is_floor=True)
    game.platforms.add(floor)
    
    # Falling player hitting floor
    game.player.pos = pygame.math.Vector2(400, 490)
    game.player.vel.y = 10
    
    game.playing = True
    game.update()
    
    assert game.playing is False
    # Depending on logic, it might set running=False or just playing=False
    # Our logic sets both
    assert game.running is True

def test_standing_no_score_increment(game):
    game.new()
    game.platforms.empty()
    
    # Normal platform
    plat = Platform(0, 300, 100, 20, is_floor=False)
    game.platforms.add(plat)
    
    # Player "standing" on platform
    game.player.pos = pygame.math.Vector2(50, 300)
    game.player.vel.y = 0 
    
    # Initial score
    game.score = 0
    
    game.update()
    
    # Should land but NOT score because we didn't "fall" significantly
    assert game.player.vel.y == 0
    assert game.score == 0

def test_initial_drop_no_score(game):
    """
    User/Game Requirement: When the actor lands on the start platform for the first time
    the score should be 0 not 10.
    """
    game.new()
    # The game loop runs updates. We need to simulate the first few frames of "landing" 
    # to see if score increments.
    
    # In Game.new(), player is spawned.
    # Let's run a few updates to simulate the drop (if we keep the drop) or just one check
    
    initial_score = game.score
    assert initial_score == 0
    
    # Simulate potential fall
    for _ in range(10):
        game.update()
        if game.player.vel.y == 0: # Landed
            break
            
    assert game.score == 0
