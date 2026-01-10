import os
import pytest
import pygame

# Set dummy video driver for headless testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for the session."""
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()
