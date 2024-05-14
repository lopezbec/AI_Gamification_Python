import json
import os
from badge_system.badge_verification import BadgeVerification

class BadgeCriteriaStreak:
    def __init__(self):
        self.streak = 0

    def correct_answer(self):
        self.streak += 1

    def incorrect_answer(self):
        self.streak = 0

    def get_current_streak(self):
        return self.streak

def display_badge(badge_details):
    badge_window = BadgeVerification(badge_details)
    badge_window.exec()

def load_badges():
    with open("badge_info.json", "r") as file:
        return json.load(file)
    
def load_badges_criteria():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "badge_criteria.json")) as content:
        return json.load(content)

def check_badges(streak):
    badges_criteria = load_badges_criteria()
    for criteria in badges_criteria:
        if streak >= criteria.get("value", 0):
            display_badge(criteria.get("badge_id"))
