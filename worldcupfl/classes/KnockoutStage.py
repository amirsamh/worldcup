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