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

def test_score_unique_platform(game):
    """
    User Requirement: A user's score should only increment if they land on a platform 
    different than the one they have jumped off.
    """
    game.new()
    initial_score = game.score
    
    # Identify start platform
    start_platform = game.last_platform
    
    # Simulate a jump and land on the SAME platform
    # We can fake the player state
    game.player.vel.y = 10 # Falling
    game.player.pos.y = start_platform.rect.top - 10 # Above
    
    # Run update to trigger collision
    game.update()
    
    # Should collide, but NOT score because it's the same platform
    assert game.player.vel.y == 0 # Landed
    assert game.score == initial_score
    
    # Now simulate moving to a NEW platform
    # Find a different platform (Game.new creates multiple)
    new_platform = None
    for p in game.platforms:
        if p != start_platform and not getattr(p, 'is_floor', False) and not getattr(p, 'moving', False):
            new_platform = p
            break
            
    if not new_platform:
        # Create one if needed
        new_platform = Platform(100, 100, 100, 20)
        game.platforms.add(new_platform)

    game.player.pos.x = new_platform.rect.centerx
    game.player.pos.y = new_platform.rect.top - 10
    game.player.vel.y = 10
    
    game.update()
    
    assert game.score == initial_score + 10 # Should score now
    assert game.last_platform == new_platform
