import json
import os

HIGHSCORE_FILE = "highscores.json"
MAX_SCORES = 5

class HighScoreManager:
    """
    Manages loading, saving, and updating the high score leaderboard.
    """
    def __init__(self, filename=HIGHSCORE_FILE):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_scores(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f)
        except IOError:
            pass # Handle error appropriately ensuring game doesn't crash

    def is_high_score(self, score):
        if score <= 0:
            return False
        if len(self.scores) < MAX_SCORES:
            return True
        # Check against the lowest score
        return score > self.scores[-1]['score']

    def add_score(self, name, score, color=(255, 255, 255)):
        # Add new score
        self.scores.append({'name': name, 'score': score, 'color': color})
        # Sort descending by score
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        # Keep top 5
        self.scores = self.scores[:MAX_SCORES]
        # Save
        self.save_scores()
