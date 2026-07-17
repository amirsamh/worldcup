#===========================
# دانشجو: سید امیرسام حسینی غنچه
# شماره دانشجویی: 404130613
# عنوان پروژه: شبیه ساز جام جهانی
# تاریخ تحویل: 
#===========================


import csv
import numpy as np
import os
import random


class Colors:
    # Color variables for better readability in terminal
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    DANGER = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class Team:
    """کلاس تیم ملی فوتبال"""
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
        """محاسبه اختلاف گل
        Returns:
            int: عدد اختلاف گل
        """
        return self.goals_for - self.goals_against
    
    def reset_stats(self):
        """ریست کردن گل ها و امتیازات تیم"""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        """شبیه‌سازی یک بازی
        Args:
            opponent (Team): تیم حریف
            is_knockout (bool): آیا مرحله حذفی است یا نه

        Returns:
            tuple: (گل های خود, گل های تیم حریف, برنده مسابقه)
        """
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
    """کلاس یک مچ بین دو تیم"""
    def __init__(self, team1, team2, is_knockout=False):
        self.is_knockout = is_knockout
        self.team1 = team1
        self.team2 = team2
        self.goals1 = None
        self.goals2 = None
        self.winner = None

    def play(self):
        """شبیه سازی کردن یک بازی بین دو تیم و مشخص کردن برنده"""
        self.goals1, self.goals2, winner_name = self.team1.simulate_match(self.team2, self.is_knockout)
        if winner_name == self.team1.name:
            self.winner = self.team1
        elif winner_name == self.team2.name:
            self.winner = self.team2
        else:
            self.winner = None


class Group:
    """کلاس گروه در مرحله گروهی"""
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        for team in self.teams:
            team.group = name
    
    def play_all_matches(self):
        """شبیه سازی تمام مچ های گروه و مشخص کردن برنده/نتیجه"""
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team_a = self.teams[i]
                team_b = self.teams[j]
                Match(team_a, team_b, is_knockout=False).play()

    def get_ranking(self):
        """برگرداندن رده بندی تیم های گروه
        
        Returns:
            list: لیست ترتیب رده بندی تیم های گروه
        """
        return sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference(), t.goals_for, random.random()),
            reverse=True
        )

    def advance_teams(self):
        """فرستادن دو تیم برتر گروه به مرحله بعد

        Returns:
            tuple: (تیم اول, تیم دوم)
        """
        ranking = self.get_ranking()
        return ranking[0], ranking[1]
    

class KnockOutStage:
    """کلاس مرحله حذفی"""
    def __init__(self, round_name, matches):
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """شبیه سازی مچ های مرحله حذفی"""
        for match in self.matches:
            match.play()

    def get_winners(self):
        """برگرداندن برنده های مرحله حذفی

        Returns:
            list: لیست برنده های مرحله حذفی
        """
        return [match.winner for match in self.matches]
    
    def display_results(self):
        """نمایش نتایج مرحله حذفی"""
        print(f"\n=============== {self.round_name} ===============")
        for match in self.matches:
            print(f"{match.team1.name} {match.goals1}-{match.goals2} {match.team2.name} -> winner: {match.winner.name}")


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

    def run_group_stage(self, should_print):
        """شبیه سازی مرحله گروهی
        
        Args:
            should_print (bool): آیا نتیجه بازی گروهی پرینت شود یا نه (برای جلوگیری از اطلاعات اضافی در شبیه سازی ۱۰۰۰ تایی)
        """
        for group in self.groups:
            group.play_all_matches()
            if should_print:
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

    def run_knockout_stage(self, should_print):
        """شبیه سازی مرحله حذفی
        
        Args:
            should_print (bool): آیا نتیجه بازی پرینت شود یا نه (برای جلوگیری از اطلاعات اضافی در شبیه سازی ۱۰۰۰ تایی)
        """
        self.round_of_16.play_round()
        if should_print:
            self.round_of_16.display_results()
        winners = self.round_of_16.get_winners()

        self.quarterfinals = KnockOutStage("Quarterfinals", [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)])
        self.quarterfinals.play_round()
        if should_print:
            self.quarterfinals.display_results()
        winners = self.quarterfinals.get_winners()

        self.semifinals = KnockOutStage("Semifinals", [Match(winners[i], winners[i+1], is_knockout=True) for i in range(0, len(winners), 2)])
        self.semifinals.play_round()
        if should_print:
            self.semifinals.display_results()
        winners = self.semifinals.get_winners()
        
        self.final = KnockOutStage("Final", [Match(winners[0], winners[1], is_knockout=True)])
        self.final.play_round()
        if should_print:
            self.final.display_results()
        self.champion = self.final.get_winners()[0]

    def run_full_simulation(self):
        """اجرای کامل شبیه سازی
        
        Returns:
            Team: تیم برنده
        """
        if self.groups != []:
            self.run_group_stage(should_print=True)
            self.setup_knockout_bracket()
            self.run_knockout_stage(should_print=True)

            print(Colors.BOLD + f"\n🏆 Champion: {self.champion.name} 🏆" + Colors.ENDC)

            return self.champion

        else:
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
                team.reset_stats()
        
            self.seed_and_draw_groups()
            self.run_group_stage(should_print=False)
            self.setup_knockout_bracket()
            self.run_knockout_stage(should_print=False)

            stats[self.champion.name] = stats.get(self.champion.name, 0) + 1

        print(f"\n=============== Champion Probabilities ===============")
        for name in sorted(stats, key=stats.get, reverse=True):
            print(f"{name}: {stats[name] / simulation_count * 100:.1f}%")

    def display_bracket(self):
        """نمایش براکت"""
        for stage in [self.round_of_16, self.quarterfinals, self.semifinals, self.final]:
            if stage:
                stage.display_results()


def main():
    sim = WorldCupSimulator()

    while True:
        print("\n=============== World Cup Simulator ===============")
        print("[1]: Load teams from CSV")
        print("[2]: Draw groups (automatic seeding)")
        print("[3]: Run group stage and display standings")
        print("[4]: Run full simulation (group + knockout) and display champion")
        print("[5]: Simulate 1000 times and report championship percentages")
        print("[6]: Display bracket of last simulation")
        print("[7]: Exit")
    
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            filename = 'worldcup_2026_teams.csv'
            try:
                sim.load_teams_from_csv(filename)
                print(Colors.GREEN + f"{len(sim.teams)} teams loaded successfully from {filename}." + Colors.ENDC)
            except Exception as e:
                print(Colors.DANGER + f"Error: {e}" + Colors.ENDC)

        elif choice == '2':
            if not sim.teams:
                print(Colors.DANGER + f"Please load teams first (option 1)." + Colors.ENDC)
            else: 
                sim.seed_and_draw_groups()
                print(Colors.GREEN + "Group draw successfull." + Colors.ENDC)

        elif choice == '3':
            if not sim.groups:
                print(Colors.DANGER + "Please draw groups first (option 2)." + Colors.ENDC)
            else:
                sim.run_group_stage(should_print=True)

        elif choice == '4':
            if not sim.teams:
                print(Colors.DANGER + "Please load teams first (option 1)." + Colors.ENDC)
            else:
                sim.run_full_simulation()

        elif choice == '5':
            if not sim.teams:
                print(Colors.DANGER + "Please load teams first (option 1)." + Colors.ENDC)
            else:
                n = 1000
                sim.most_likely_champion(n)

        elif choice == '6':
            if not sim.round_of_16:
                print(Colors.DANGER + "Please run a full simulation first (option 4)." + Colors.ENDC)
            else:
                sim.display_bracket()

        elif choice == '7':
            break

        else:
            print(Colors.WARNING + "Invalid option." + Colors.ENDC)


if __name__ == "__main__":
    main()