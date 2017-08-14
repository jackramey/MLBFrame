import json
import logging
import requests

from mlbframe import app
from .models import Game, Team


log = logging.getLogger()
console = logging.StreamHandler
log.addHandler(console)


def get_master_scoreboard(year, month, day):
    y = str(year)
    m = str(month).zfill(2)
    d = str(day).zfill(2)
    url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/master_scoreboard.json".format(y, m, d)
    log.info("Scoreboard URL: {0}".format(url))
    app.logger.info("Scoreboard URL: {0}".format(url))
    data = None
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = json.loads(resp.text)
    except requests.HTTPError:
        app.logger.info("Invalid data given.")
    return data


def get_boxscore(game_id):
    y, m, d, tail = game_id.split('_', 3)
    url = "http://gd2.mlb.com/components/game/mlb" + \
          "/year_{0}/month_{1}/day_{2}/gid_{3}/boxscore.json".format(y, m, d, game_id)
    log.info("Boxscore URL: {0}".format(url))
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = json.loads(resp.text)
    except requests.HTTPError:
        raise ValueError("Invalid Game ID")

    return data

