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