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