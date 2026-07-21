import csv
import numpy as np
import random
from .Group import Group
from .Match import Match
from .Team import Team
from .KnockoutStage import KnockOutStage


class WorldCupSimulator:
    """کلاس اجرای شبیه ساز جام جهانی"""
    def __init__(self):
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def load_teams_from_csv(self, filename):
        """خواندن اطلاعات از فایل
        
        Args:
            filename (str): نام فایل
        """
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
        """قرعه کشی گروه"""
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
        """شبیه سازی مرحله گروهی
        
        Returns:
            data (dict): نتایج هر تیم در مرحله گروهی
        """
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
        """چیدن براکت مرحله حذفی"""
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
        """شبیه سازی مرحله حذفی"""
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
        """اجرای کامل شبیه سازی
        
        Returns:
            Team: تیم برنده
        """
        for team in self.teams:
            team.reset_stats()

        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()

        return self.champion

    def most_likely_champion(self, simulation_count=1000):
        """تکرار شبیه سازی به تعداد دلخواه (دیفالت ۱۰۰۰)"""
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
        """نمایش براکت"""
        for stage in [self.round_of_16, self.quarterfinals, self.semifinals, self.final]:
            if stage:
                stage.display_results()