import pytest
import pygame
from unittest.mock import MagicMock, patch
from main import Game
from settings import *

@pytest.fixture
def game():
    return Game()

def test_game_init(game):
    assert game.running is True
    assert game.screen_width == SCREEN_WIDTH
    assert game.screen_height == SCREEN_HEIGHT

def test_new_game(game):
    # Mock run so it doesn't start the loop
    game.run = MagicMock()
    game.new()
    assert len(game.all_sprites) > 0
    assert len(game.platforms) > 0
    assert game.player is not None

def test_update_collision(game):
    game.run = MagicMock()
    game.new()
    # Place player above platform (use index 1 which is not floor)
    platform = game.platforms.sprites()[1]
    game.player.pos = pygame.math.Vector2(platform.rect.centerx, platform.rect.top - 10)
    game.player.vel.y = 10 # Falling
    
    game.update()
    
    # Should snap to platform
    assert game.player.pos.y == platform.rect.top
    assert game.player.vel.y == 0

def test_sticky_platform_collision(game):
    game.run = MagicMock()
    game.new()
    # Clear existing platforms to avoid interference
    game.platforms.empty()
    
    # Create a moving platform
    from sprites import Platform
    moving_plat = Platform(100, 300, 100, 20, moving=True)
    game.platforms.add(moving_plat)
    game.all_sprites.add(moving_plat)
    
    # Place player landing on it
    game.player.pos = pygame.math.Vector2(150, 290)
    game.player.vel.y = 10
    
    # Perform update
    initial_player_x = game.player.pos.x
    moving_plat.velocity = 5 # Force velocity
    
    game.update()
    
    # Player should have moved with platform
    assert game.player.pos.x == initial_player_x + 5
    assert game.player.vel.y == 0

@patch('pygame.event.get')
def test_quit_event(mock_event_get, game):
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    mock_event_get.return_value = [mock_event]
    
    game.playing = True
    game.events()
    
    assert game.playing is False
    assert game.running is False

@patch('pygame.event.get')
def test_jump_event(mock_event_get, game):
    game.run = MagicMock()
    game.new()
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_SPACE
    mock_event_get.return_value = [mock_event]
    
    # Mock player jump
    game.player.jump = MagicMock()
    
    game.events()
    
    game.player.jump.assert_called_once()
