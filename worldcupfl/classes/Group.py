import random
from .Match import Match


class Group:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        for team in self.teams:
            team.group = name
    
    def play_all_matches(self):
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team_a = self.teams[i]
                team_b = self.teams[j]
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