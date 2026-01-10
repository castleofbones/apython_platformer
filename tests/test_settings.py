from settings import *

def test_screen_settings():
    assert isinstance(SCREEN_WIDTH, int)
    assert isinstance(SCREEN_HEIGHT, int)
    assert isinstance(SCREEN_TITLE, str)
    assert isinstance(FPS, int)

def test_colors():
    assert len(WHITE) == 3
    assert len(BLACK) == 3
    assert len(RED) == 3
    assert len(GREEN) == 3
    assert len(BLUE) == 3
    assert len(YELLOW) == 3

def test_physics_settings():
    assert isinstance(PLAYER_ACC, float)
    assert isinstance(PLAYER_FRICTION, float)
    assert isinstance(PLAYER_GRAVITY, float)
    assert isinstance(PLAYER_JUMP, int)

def test_game_settings():
    assert FONT_NAME == 'Cascadia Code'
    assert isinstance(SCREEN_DELAY, int)
    assert isinstance(PLATFORM_MOVE_DURATION, int)
    assert isinstance(VERSION, str)
