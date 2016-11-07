# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ATXItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    league = Field()
    team = Field()
    home = Field()
    away = Field()
    comp = Field()
    date = Field()
    mid = Field()
    score = Field()


class BTXItem(Item):
    home = Field()
    away = Field()
    comp = Field()
    date = Field()
    mid = Field()
    score = Field()
    possession = Field()
    passing = Field()
    cross = Field()
    shoot = Field()
    shot_on = Field()
    tackle = Field()
    corner = Field()
    free_kick = Field()
    offside = Field()
    foul = Field()
    yel_card = Field()
    red_card = Field()
    formation = Field()
    game_time = Field()
    home_goaler = Field()
    away_goaler = Field()
    home_players = Field()
    away_players = Field()

class ASodaItem(Item):
    team = Field()
    match = Field()
    home_away = Field()
    comp = Field()
    date = Field()
    goal = Field()
    mid = Field()
    score = Field()

class BSodaItem(Item):
    season = Field()
    teams = Field()
    comp = Field()
    date = Field()
    mid = Field()
    score = Field()
    round = Field()
    possession = Field()
    passing = Field()
    cross = Field()
    shoot = Field()
    shot_on = Field()
    shot_post = Field()
    tackle = Field()
    corner = Field()
    offside = Field()
    saves = Field()
    yel_card = Field()
    red_card = Field()
    formation = Field()
    referee = Field()
    home_goaler = Field()
    away_goaler = Field()
    home_player = Field()
    away_player = Field()
    home_action = Field()
    away_action = Field()