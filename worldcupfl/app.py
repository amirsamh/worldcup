from flask import Flask, render_template
from classes.WorldCupSimulator import WorldCupSimulator

app = Flask(__name__)
sim = WorldCupSimulator()
sim.load_teams_from_csv('worldcup_2026_teams.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/draw')
def draw():
    sim.groups = []
    sim.seed_and_draw_groups()
    groups = [{'name': group.name, 'teams': [t.name for t in group.teams]} for group in sim.groups]
    return render_template('draw.html', groups=groups)


@app.route('/group-stage')
def group_stage():
    if sim.groups != []:
        for team in sim.teams:
            team.reset_stats()
        sim.run_group_stage()
        groups = [
            {
                'name': group.name,
                'teams': [
                    {
                        'name': team.name,
                        'points': team.points,
                        'gf': team.goals_for,
                        'ga': team.goals_against,
                        'gd': team.goal_difference()
                    }
                    for team in group.get_ranking()
                ]
            }
            for group in sim.groups
        ]
        return render_template('group_stage.html', groups=groups)
    else:
        return render_template('index.html', error='ابتدا قرعه کشی گروه ها را انجام دهید')
 

@app.route('/full-simulation')
def full_simulation():
    if sim.groups != []:
        champion = sim.run_full_simulation()
        bracket = []
        for stage in [sim.round_of_16, sim.quarterfinals, sim.semifinals, sim.final]:
            matches = [
                {
                    'team1': m.team1.name,
                    'goals1': m.goals1,
                    'team2': m.team2.name,
                    'goals2': m.goals2,
                    'winner': m.winner.name
                }
                for m in stage.matches
            ]
            bracket.append({'round_name': stage.round_name, 'matches': matches})
        return render_template('full_simulation.html', champion=champion.name, bracket=bracket)
    else:
        return render_template('index.html', error='ابتدا قرعه کشی گروه ها را انجام دهید')
 

@app.route('/most-likely')
def most_likely():
    if sim.groups != []:
        stats = sim.most_likely_champion(1000)
        results = [
            {'name': name, 'percentage': round(count / 1000 * 100, 1)}
            for name in sorted(stats, key=stats.get, reverse=True)
            for count in [stats[name]]
        ]
        return render_template('most_likely.html', results=results)
    else:
        return render_template('index.html', error='ابتدا قرعه کشی گروه ها را انجام دهید')


@app.route('/bracket')
def bracket():
    if sim.groups != []:
        if not sim.round_of_16:
            return render_template('bracket.html', bracket=None)
        bracket = []
        for stage in [sim.round_of_16, sim.quarterfinals, sim.semifinals, sim.final]:
            matches = [
                {
                    'team1': m.team1.name,
                    'goals1': m.goals1,
                    'team2': m.team2.name,
                    'goals2': m.goals2,
                    'winner': m.winner.name
                }
                for m in stage.matches
            ]
            bracket.append({'round_name': stage.round_name, 'matches': matches})
        return render_template('bracket.html', bracket=bracket)
    else:
        return render_template('index.html', error='ابتدا قرعه کشی گروه ها را انجام دهید')


if __name__ == "__main__":
    app.run()