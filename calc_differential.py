import mlbframe.models as models
import matplotlib.pyplot as plt
import numpy as np

from sqlalchemy import and_, or_


def calculate(team_abbrev):
    differentials = []
    team_id = models.Team.query.filter(models.Team.abbrev == team_abbrev).first().id
    games = models.Game.query.filter(and_(or_(
        models.Game.away_team_id == team_id,
        models.Game.home_team_id == team_id),
        models.Game.game_type == 'R')
    ).order_by(models.Game.id)
    for game in games:
        if game.away_team_id == team_id:
            differentials.append(game.away_win - game.away_loss)
        else:
            differentials.append(game.home_win - game.home_loss)
    return differentials

if __name__ == "__main__":
    diffs = {}
    teams = models.Team.query.all()
    for team in teams:
        diff = calculate(team.abbrev)[:80]
        print(team.abbrev)
        print(len(diff))
        diffs[team.abbrev] = np.array(diff)
        print("{0} - {1}".format(team.abbrev, team.name))
        print(diffs[team.abbrev])
    X = range(0, 80)

    plt.axhline(y=0, color='gray', linestyle='-')

    plt.plot(X, diffs['SF'], color="orange", label='SF')
    plt.plot(X, diffs['LAD'], color="blue", label='LAD')
    plt.plot(X, diffs['COL'], color="purple", label='COL')
    plt.plot(X, diffs['SD'], color="black", label='SD')
    plt.plot(X, diffs['ARI'], color="red", label='ARI')

    plt.legend()

    plt.show()
