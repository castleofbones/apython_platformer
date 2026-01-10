import pytest
import os
import json
from highscore_manager import HighScoreManager

TEST_FILE = "test_highscores.json"

@pytest.fixture
def manager():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    mgr = HighScoreManager(TEST_FILE)
    yield mgr
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_empty_init(manager):
    assert manager.scores == []
    assert manager.is_high_score(100) is True

def test_add_score(manager):
    manager.add_score("AAA", 100)
    assert len(manager.scores) == 1
    assert manager.scores[0]['score'] == 100
    assert manager.scores[0]['name'] == "AAA"
    
    # Verify persistence
    mgr2 = HighScoreManager(TEST_FILE)
    assert len(mgr2.scores) == 1
    assert mgr2.scores[0]['score'] == 100

def test_add_score_with_color(manager):
    color = (255, 0, 0)
    manager.add_score("RED", 200, color)
    assert manager.scores[0]['color'] == list(color) or manager.scores[0]['color'] == tuple(color)
    
    # Persistence
    mgr2 = HighScoreManager(TEST_FILE)
    loaded_color = mgr2.scores[0]['color']
    # JSON loads tuples as lists
    assert tuple(loaded_color) == color

def test_is_high_score(manager):
    manager.add_score("A", 100)
    assert manager.is_high_score(50) is True # Still have room
    
    manager.add_score("B", 80)
    manager.add_score("C", 60)
    manager.add_score("D", 40)
    manager.add_score("E", 20)
    # List is full: 100, 80, 60, 40, 20
    
    assert manager.is_high_score(10) is False # Lower than 20
    assert manager.is_high_score(30) is True # Higher than 20

def test_score_sorting_and_trimming(manager):
    scores = [10, 20, 30, 40, 50, 60]
    for s in scores:
        manager.add_score("TEST", s)
        
    assert len(manager.scores) == 5
    assert manager.scores[0]['score'] == 60
    assert manager.scores[-1]['score'] == 20
