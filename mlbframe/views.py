import datetime
import json

from flask import render_template, request
from sqlalchemy import and_

from mlbframe import app
from mlbframe.team_colors import team_colors
from mlbframe.models import Meta, Team
from mlbframe.RecordDifferentialCalculator import calculate


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/differentials")
def getValues():
    meta = Meta.query.order_by(Meta.id).first()
    if meta.last_updated < datetime.date.today():
        from mlbframe import build_db
        build_db.update()
    data = {'data': []}
    year = request.args.get('year')
    year = year if year is not None else datetime.datetime.today().year
    team_params = set(request.args.getlist('team'))
    division_param = request.args.get('division')
    if division_param is not None:
        league = division_param[0:2]
        div = division_param[2]
        div_teams = Team.query.filter(and_(Team.league == league.upper(),
                                           Team.division == div.upper())
                                      ).all()
        for div_team in div_teams:
            team_params.add(div_team.abbrev)

    for team_param in team_params:
        team = Team.query.filter(Team.abbrev == team_param).first()
        team_data = {'id': team.id, 'abbrev': team.abbrev, 'color': team_colors[team.abbrev]}
        diffs = calculate(team.abbrev, year)
        team_data = {'team': team_data, 'differentials': diffs}
        data['data'].append(team_data)

    return json.dumps(data)
