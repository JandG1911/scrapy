# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import hashlib
import re
import logging
from scrapy.conf import settings
from football.items import ASodaItem, BSodaItem
from football.items import ATXItem, BTXItem

class FootballPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.league = {'8': 'Premier_League', '21': 'Serie_A', '22': 'Bundesliga', '23': 'La_Liga', '24': 'Ligue_1', '208': 'CSL'}

    def process_item(self, item, spider):
        if isinstance(item, ATXItem):
            match = item['away'] if item['home'] == item['team'] else item['home']
            home_or_away = 'HOME' if item['home'] == item['team'] else 'AWAY'
            hashed = self.hashed(item['team'], item['mid'])
            home = int(re.search('^\d+', item['score']).group())
            away = int(re.search('\d+$', item['score']).group())
            if home > away and home_or_away == 'HOME':
                outcome = 'Win'
            elif home > away and home_or_away == 'AWAY':
                outcome = 'Lose'
            elif home < away and home_or_away == 'HOME':
                outcome = 'Lose'
            elif home < away and home_or_away == 'AWAY':
                outcome = 'Win'
            else:
                outcome = 'Draw'

            team_item = {
                '_id': item['mid'],
                '胜负': outcome,
                '对手': match,
                '主客': home_or_away,
                '赛事': item['comp'],
                '开场时间': item['date'],
                '比分': item['score'],
            }
            try:
                self.client['FOOTBALL']['hash-TX'].insert({'_id': item['mid'],
                                                                'hash': hashed,
                                                                '球队': item['team'],
                                                                })
                team = self.client[self.league[item['league']]][item['team']]
                team.insert(team_item)
            except:
                logging.info('insert error:{} - {}'.format(item['team'], item['mid']))

        if isinstance(item, BTXItem):
            try:
                game_item = {
                    '_id': item['mid'],
                    '球队': '{0} - {1}'.format(item['home'], item['away']),
                    '赛事': item['comp'],
                    '开场时间': item['date'],
                    '比分': item['score'],
                    '控球率': item['possession'],
                    '传球': item['passing'],
                    '传中': item['cross'],
                    '射门': item['shoot'],
                    '射正': item['shot_on'],
                    '抢断': item['tackle'],
                    '角球': item['corner'],
                    '任意球': item['free_kick'],
                    '越位': item['offside'],
                    '犯规': item['foul'],
                    '黄牌': item['yel_card'],
                    '红牌': item['red_card'],
                    '阵型': item['formation'],
                    '比赛时长': item['game_time'],
                    '主队球员': item['home_players'],
                    '客队球员': item['away_players'],
                    '主队进球者': item['home_goaler'],
                    '客队进球者': item['away_goaler'],
                }
                game = self.client['FOOTBALL']['game-TX']
                game.insert(game_item)
            except:
                logging.info('insert error: {} - {}'.format(item['team'], item['mid']))
        return item

    def hashed(self, one, two):
        m = hashlib.md5()
        pwd = (one + two).encode('utf-8')
        m.update(pwd)
        return m.hexdigest()


class SodaPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        self.client = pymongo.MongoClient(host=host, port=port)

    def process_item(self, item, spider):
        if isinstance(item, ASodaItem):
            hashed = self.hashed(item['team'], item['mid'])
            home = int(re.search('^\d+', item['score']).group())
            away = int(re.search('\d+$', item['score']).group())
            if home > away and item['home_away'] == 'home':
                outcome = 'Win'
            elif home > away and item['home_away'] == 'away':
                outcome = 'Lose'
            elif home < away and item['home_away'] == 'home':
                outcome = 'Lose'
            elif home < away and item['home_away'] == 'away':
                outcome = 'Win'
            else:
                outcome = 'Draw'

            try:
                self.client['FOOTBALL']['hash-soda'].insert({'_id': hashed,
                                                        '球队': item['team'],
                                                         'mid': item['mid'],
                                                         })
                team_item = {
                    '_id': item['mid'],
                    '胜负': outcome,
                    '主客': item['home_away'].upper(),
                    '开场时间': item['date'],
                    '比分': item['score'],
                    '对手': item['match'],
                    '赛事': item['comp'],
                    '进球者': item['goal'],
                }
                team = self.client[item['comp']][item['team']]
                team.insert(team_item)
            except Exception as e:
                logging.info('{} - {}'.format(e, item['mid']))

        if isinstance(item, BSodaItem):
            try:
                game_item = {
                    '_id': item['mid'],
                    '赛季': item['season'],
                    '球队': item['teams'],
                    '赛事': item['comp'],
                    '开场时间': item['date'],
                    '裁判': item['referee'],
                    '轮次': item['round'],
                    '比分': item['score'],
                    '控球率': item['possession'],
                    '传球': item['passing'],
                    '传中': item['cross'],
                    '射门': item['shoot'],
                    '射正': item['shot_on'],
                    '门柱': item['shot_post'],
                    '抢断': item['tackle'],
                    '角球': item['corner'],
                    '越位': item['offside'],
                    '黄牌': item['yel_card'],
                    '红牌': item['red_card'],
                    '阵型': item['formation'],
                    '扑救': item['saves'],
                    '主队球员': item['home_player'],
                    '客队球员': item['away_player'],
                    '主队进球者': item['home_goaler'],
                    '客队进球者': item['away_goaler'],
                    '主队动态': item['home_action'],
                    '客队动态': item['away_action'],
                }
                game = self.client['FOOTBALL']['game-soda']
                game.insert(game_item)
            except Exception as e:
                logging.info('{}'.format(e))
        return item

    def hashed(self, one, two):
        m = hashlib.md5()
        pwd = (one + two).encode('utf-8')
        m.update(pwd)
        return m.hexdigest()