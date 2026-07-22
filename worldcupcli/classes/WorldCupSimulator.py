import csv
import random
from .Colors import Colors
from .Group import Group
from .KnockOutStage import KnockOutStage
from .Match import Match
from .Team import Team


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
                team = Team( # Set each line of the CSV file to a Team class
                    name=row['name'],
                    attack=int(row['attack']),
                    defense=int(row['defense']),
                    rank=int(row['rank'])
                )
                self.teams.append(team)
        
    def seed_and_draw_groups(self):
        """قرعه کشی گروه"""
        sorted_teams = sorted(self.teams, key=lambda t: t.rank) # Sort teams based on FIFA rankings
        seed1 = sorted_teams[0:8] 
        seed2 = sorted_teams[8:16]
        seed3 = sorted_teams[16:24]
        seed4 = sorted_teams[24:32]

        random.shuffle(seed1) # Shuffle the order of each group's teams
        random.shuffle(seed2)
        random.shuffle(seed3)
        random.shuffle(seed4)

        for i, name in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']): # Add alphabetical names to groups
            self.groups.append(Group(name, [seed1[i], seed2[i], seed3[i], seed4[i]]))

    def run_group_stage(self, should_print):
        """شبیه سازی مرحله گروهی
        
        Args:
            should_print (bool): آیا نتیجه بازی گروهی پرینت شود یا نه (برای جلوگیری از اطلاعات اضافی در شبیه سازی ۱۰۰۰ تایی)
        """
        for group in self.groups:
            group.play_all_matches() # Play all group matches
            if should_print: # Only print the result if needed - used to prevent things getting messy in 1000 simulation
                print(f"\n=============== Group {group.name} ===============")
                for i, team in enumerate(group.get_ranking(), 1):
                    print(f"{i}. {team.name} Pts:{team.points}  GF:{team.goals_for}  GA:{team.goals_against}  GD:{team.goal_difference()}")

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

        matches = [ # Matching based on FIFA rules - A1 vs B2, C1 vs D2, E1 vs F2, G1 vs H2, B1 vs A2, D1 vs C2, F1 vs E2, H1 vs G2
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

    def run_knockout_stage(self, should_print):
        """شبیه سازی مرحله حذفی
        
        Args:
            should_print (bool): آیا نتیجه بازی پرینت شود یا نه (برای جلوگیری از اطلاعات اضافی در شبیه سازی ۱۰۰۰ تایی)
        """
        self.round_of_16.play_round()
        if should_print: # Only print the result if needed - used to prevent things getting messy in 1000 simulation
            self.round_of_16.display_results()
        winners = self.round_of_16.get_winners()

        self.quarterfinals = KnockOutStage(
            "Quarterfinals", 
            [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)] # Matching the winners of the previous round
        )
        self.quarterfinals.play_round()
        if should_print:
            self.quarterfinals.display_results()
        winners = self.quarterfinals.get_winners()

        self.semifinals = KnockOutStage(
            "Semifinals", 
            [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)]
        )
        self.semifinals.play_round()
        if should_print:
            self.semifinals.display_results()
        winners = self.semifinals.get_winners()
        
        self.final = KnockOutStage(
            "Final", 
            [Match(winners[0], winners[1], is_knockout=True)]
        )
        self.final.play_round()
        if should_print:
            self.final.display_results()
        self.champion = self.final.get_winners()[0]

    def run_full_simulation(self):
        """اجرای کامل شبیه سازی
        
        Returns:
            Team: تیم برنده
        """
        if self.groups != []: # Prevent seeding and drawing groups when it is already done
            self.run_group_stage(should_print=True)
            self.setup_knockout_bracket()
            self.run_knockout_stage(should_print=True)

            print(Colors.BOLD + f"\n🏆 Champion: {self.champion.name} 🏆" + Colors.ENDC)

            return self.champion

        else: # Ask user to draw groups before running full simulation if they never have
            print(Colors.DANGER + "Please draw groups first (option 2)." + Colors.ENDC)

    def most_likely_champion(self, simulation_count=1000):
        """تکرار شبیه سازی به تعداد دلخواه (دیفالت ۱۰۰۰)
        
        Args:
            simulation_count (int): تعداد دفعات شبیه سازی
        """
        stats = {}
        for i in range(simulation_count):
            print(f"simulation {i} completed.")
            for team in self.teams:
                team.reset_stats() # Clear the last simulation before proceeding
        
            self.seed_and_draw_groups()
            self.run_group_stage(should_print=False)
            self.setup_knockout_bracket()
            self.run_knockout_stage(should_print=False)

            stats[self.champion.name] = stats.get(self.champion.name, 0) + 1

        print(f"\n=============== Champion Probabilities ===============")
        for name in sorted(stats, key=stats.get, reverse=True):
            print(f"{name}: {stats[name] / simulation_count * 100:.1f}%") # Display probability percentage with one decimal place 

    def display_bracket(self):
        """نمایش براکت"""
        for stage in [self.round_of_16, self.quarterfinals, self.semifinals, self.final]:
            if stage:
                stage.display_results()