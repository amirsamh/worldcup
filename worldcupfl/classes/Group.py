import random
from .Match import Match


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
            key=lambda t: (t.points, t.goal_difference(), t.goals_for, random.random()), # Sort by points/GD/GF or randomly
            reverse=True
        )

    def advance_teams(self):
        """فرستادن دو تیم برتر گروه به مرحله بعد

        Returns:
            tuple: (تیم اول, تیم دوم)
        """
        ranking = self.get_ranking()
        return ranking[0], ranking[1] # Advance the first two teams of the group