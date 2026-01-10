import pygame
import pytest
from sprites import Player
from main import Game
from settings import RED, BLUE, YELLOW

def test_player_init_color():
    game = Game()
    
    # Default (Yellow)
    p_def = Player(game)
    assert p_def.image.get_at((0,0)) == YELLOW
    
    # Explicit Red
    p_red = Player(game, color=RED)
    assert p_red.image.get_at((0,0)) == RED
    
    # Explicit Blue
    p_blue = Player(game, color=BLUE)
    assert p_blue.image.get_at((0,0)) == BLUE

def test_game_color_storage():
    game = Game()
    assert game.player_color == YELLOW # Default
    
    # Simulate selection
    game.player_color = BLUE
    game.new() # Should create player with BLUE
    
    assert game.player.image.get_at((0,0)) == BLUE
