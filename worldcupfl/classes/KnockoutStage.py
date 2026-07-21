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
        """نمایش نتایج مرحله حذفی
        
        Returns:
            dict: اطلاعات هر مرحله از مراحل حذفی
        """
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