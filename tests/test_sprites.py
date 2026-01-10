import pytest
import pygame
from unittest.mock import patch, MagicMock
from sprites import Player, Platform
from settings import *

def test_platform_init():
    p = Platform(0, 0, 100, 20)
    assert p.rect.x == 0
    assert p.rect.y == 0
    assert p.rect.width == 100
    assert p.rect.height == 20
    assert p.moving is False

def test_moving_platform_init():
    p = Platform(0, 0, 100, 20, moving=True)
    assert p.moving is True
    assert p.start_x == 0
    assert p.velocity != 0

def test_moving_platform_update():
    p = Platform(0, 0, 100, 20, moving=True)
    initial_x = p.rect.x
    p.update()
    assert p.rect.x != initial_x

class MockGame:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

def test_player_init():
    game = MockGame()
    p = Player(game)
    assert p.game == game
    assert p.vel.x == 0
    assert p.vel.y == 0
    assert p.acc.x == 0

@patch('pygame.key.get_pressed')
def test_player_movement_physics(mock_get_pressed):
    game = MockGame()
    p = Player(game)
    
    # Mock key press
    # Create a mock that returns True only for K_RIGHT
    mock_keys = MagicMock()
    def get_key(k):
        return k == pygame.K_RIGHT
    mock_keys.__getitem__.side_effect = get_key
    mock_get_pressed.return_value = mock_keys

    p.update()
    
    assert p.vel.x > 0 # Should gain velocity
    assert p.pos.x > 10 # Should move right from initial pos

def test_player_screen_wrap():
    game = MockGame()
    p = Player(game)
    p.pos.x = SCREEN_WIDTH + 10
    p.update()
    assert p.pos.x == 0
    
    p.pos.x = -10
    p.update()
    assert p.pos.x == SCREEN_WIDTH
