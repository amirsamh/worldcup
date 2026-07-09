from flask import Flask, render_template
from worldcup_simulator import WorldCupSimulator

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
 

@app.route('/full-simulation')
def full_simulation():
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
 

@app.route('/most-likely')
def most_likely():
    stats = sim.most_likely_champion(1000)
    results = [
        {'name': name, 'percentage': round(count / 1000 * 100, 1)}
        for name in sorted(stats, key=stats.get, reverse=True)
        for count in [stats[name]]
    ]
    return render_template('most_likely.html', results=results)


@app.route('/bracket')
def bracket():
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


if __name__ == "__main__":
    app.run()