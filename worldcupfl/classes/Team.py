import numpy as np
import random


class Team:
    def __init__(self, name, attack, defense, rank):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None

    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    def reset_stats(self):
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opp = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        goals_self = int(np.random.poisson(lambda_self))
        goals_opponent = int(np.random.poisson(lambda_opp))

        self.goals_for += goals_self
        self.goals_against += goals_opponent
        opponent.goals_for += goals_opponent
        opponent.goals_against += goals_self

        if goals_self > goals_opponent:
            winner = self.name
            if not is_knockout:
                self.points += 3
        elif goals_self < goals_opponent:
            winner = opponent.name
            if not is_knockout:
                opponent.points += 3
        else:
            if is_knockout:
                p_self = np.clip(0.75 + (self.attack - opponent.defense) / 250, 0.6, 0.9)
                p_opp = np.clip(0.75 + (opponent.attack - self.defense) / 250, 0.6, 0.9)

                self_pens, opp_pens = 0, 0

                for _ in range(5):
                    self_pens += random.random() < p_self
                    opp_pens += random.random() < p_opp

                while self_pens == opp_pens:
                    self_pens += random.random() < p_self
                    opp_pens += random.random() < p_opp

                winner = self.name if self_pens > opp_pens else opponent.name
            else:
                winner = None
                self.points += 1
                opponent.points += 1

        return goals_self, goals_opponent, winner