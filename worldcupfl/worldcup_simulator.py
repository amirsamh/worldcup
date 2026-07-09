import csv
from itertools import combinations
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
    

class Match:
    def __init__(self, team1, team2, is_knockout=False):
        self.is_knockout = is_knockout
        self.team1 = team1
        self.team2 = team2
        self.goals1 = None
        self.goals2 = None
        self.winner = None

    def play(self):
        self.goals1, self.goals2, winner_name = self.team1.simulate_match(self.team2, self.is_knockout)
        if winner_name == self.team1.name:
            self.winner = self.team1
        elif winner_name == self.team2.name:
            self.winner = self.team2
        else:
            self.winner = None


class Group:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        for team in self.teams:
            team.group = name
    
    def play_all_matches(self):
        for team_a, team_b in combinations(self.teams, 2):
            Match(team_a, team_b, is_knockout=False).play()

    def get_ranking(self):
        return sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference(), t.goals_for, random.random()),
            reverse=True
        )

    def advance_teams(self):
        ranking = self.get_ranking()
        return ranking[0], ranking[1]
    

class KnockOutStage:
    def __init__(self, round_name, matches):
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        for match in self.matches:
            match.play()

    def get_winners(self):
        return [match.winner for match in self.matches]
    
    def display_results(self):
        return {
            'round_name': self.round_name,
            'matches': [
                {
                    'team1': match.team1.name,
                    'goals1': match.goals1,
                    'team2': match.team2.name,
                    'goals2': match.goals2,
                    'winner': match.winner.name
                }
                for match in self.matches
            ]
        }


class WorldCupSimulator:
    def __init__(self):
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def load_teams_from_csv(self, filename):
        self.teams = []
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                team = Team(
                    name=row['name'],
                    attack=int(row['attack']),
                    defense=int(row['defense']),
                    rank=int(row['rank'])
                )
                self.teams.append(team)
        
    def seed_and_draw_groups(self):
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)
        seed1 = sorted_teams[0:8]
        seed2 = sorted_teams[8:16]
        seed3 = sorted_teams[16:24]
        seed4 = sorted_teams[24:32]

        random.shuffle(seed1)
        random.shuffle(seed2)
        random.shuffle(seed3)
        random.shuffle(seed4)

        for i, name in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            self.groups.append(Group(name, [seed1[i], seed2[i], seed3[i], seed4[i]]))

    def run_group_stage(self):
        for group in self.groups:
            group.play_all_matches()

            data = {}

            for team in group.get_ranking():
                data[team] = {
                    'team_name': team.name,
                    'gf': team.goals_for,
                    'ga': team.goals_against,
                    'gd': team.goal_difference()
                }

        return data


    def setup_knockout_bracket(self):
        advanced_teams = [group.advance_teams() for group in self.groups]

        a1, a2 = advanced_teams[0]
        b1, b2 = advanced_teams[1]
        c1, c2 = advanced_teams[2]
        d1, d2 = advanced_teams[3]
        e1, e2 = advanced_teams[4]
        f1, f2 = advanced_teams[5]
        g1, g2 = advanced_teams[6]
        h1, h2 = advanced_teams[7]

        matches = [
            Match(a1, b2, is_knockout=True),
            Match(c1, d2, is_knockout=True),
            Match(e1, f2, is_knockout=True),
            Match(g1, h2, is_knockout=True),
            Match(b1, a2, is_knockout=True),
            Match(d1, c2, is_knockout=True),
            Match(f1, e2, is_knockout=True),
            Match(h1, g2, is_knockout=True),
        ]

        self.round_of_16 = KnockOutStage("Round of 16", matches)

    def run_knockout_stage(self):
        self.round_of_16.play_round()
        self.round_of_16.display_results()
        winners = self.round_of_16.get_winners()

        self.quarterfinals = KnockOutStage("Quarterfinals", [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)])
        self.quarterfinals.play_round()
        self.quarterfinals.display_results()
        winners = self.quarterfinals.get_winners()

        self.semifinals = KnockOutStage("Semifinals", [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)])
        self.semifinals.play_round()
        self.semifinals.display_results()
        winners = self.semifinals.get_winners()
        
        self.final = KnockOutStage("Final", [Match(winners[0], winners[1], is_knockout=True)])
        self.final.play_round()
        self.final.display_results()
        self.champion = self.final.get_winners()[0]

    def run_full_simulation(self):
        for team in self.teams:
            team.reset_stats()
        
        self.seed_and_draw_groups()
        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()

        return self.champion

    def most_likely_champion(self, simulation_count=1000):
        stats = {}
        for i in range(simulation_count):
            for team in self.teams:
                team.reset_stats()
            self.groups = []
            self.seed_and_draw_groups()
            self.run_group_stage()
            self.setup_knockout_bracket()
            self.run_knockout_stage()
            stats[self.champion.name] = stats.get(self.champion.name, 0) + 1
        return stats


    def display_bracket(self):
        for stage in [self.round_of_16, self.quarterfinals, self.semifinals, self.final]:
            if stage:
                stage.display_results()