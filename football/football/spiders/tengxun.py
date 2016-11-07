# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import json
import re
import logging
import pymongo
from scrapy.http import Request
from football.items import ATXItem, BTXItem



class ClubSpider(scrapy.Spider):
    name = "tengxun"
    allowed_domains = ["qq.com"]
    start_urls = (
        'http://soccerdata.sports.qq.com/leagrank/8/jifen.htm',
        'http://soccerdata.sports.qq.com/leagrank/23/jifen.htm',
        'http://soccerdata.sports.qq.com/leagrank/22/jifen.htm',
        'http://soccerdata.sports.qq.com/leagrank/21/jifen.htm',
        'http://soccerdata.sports.qq.com/leagrank/24/jifen.htm',
        'http://soccerdata.sports.qq.com/leagrank/208/jifen.htm'
    )
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'soccerdata.sports.qq.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
        },
        'ITEM_PIPELINES': {
            'football.pipelines.FootballPipeline': 100,
        }
    }
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.mid = client['FOOTBALL']['hash-tengxun']
        self.client = client

    def parse(self, response):
        league = re.search('rank/(\d+)/jifen', response.url, re.S).group(1)
        for team in response.xpath('//div[@class="mContTab"]/table[1]/tr[@class="a2"]'):
            link = team.xpath('td[@class="oCol"]/a/@href').extract()[0]
            yield Request(link, callback=self.parse_team, meta={'league': league})

    def parse_team(self, response):
        league = response.meta['league']
        team = response.xpath('//div[@class="mLeftTop"]/h2/text()').re('(\S+)')[0]
        for game in response.xpath('//div[@class="season-stat"]/div[2]/table[2]/tr[@class="a2"]'):
            date = game.xpath('td[1]/text()').extract()[0]
            d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
            if int(time.time()) >= int(time.mktime(d.timetuple())):
                mid = game.xpath('td[@class="a3"]/strong/a/@href').re('mid=(\d+)')[0]
                if self.mid.find_one({'_id': mid}) == None:
                    header = {
                        'Referer': 'http://soccerdata.sports.qq.com/live.htm?mid={}'.format(mid),
                        'Accept': 'application/json, text/javascript, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Origin': 'http://soccerdata.sports.qq.com',
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                    link = 'http://soccerdata.sports.qq.com/s/live.action?mid={}'.format(mid)
                    yield Request(link, callback=self.parse_game, headers=header)
                item = ATXItem()
                item['home'] = game.xpath('td[3]/span/a/text()').extract()[0]
                item['away'] = game.xpath('td[5]/span/a/text()').extract()[0]
                item['score'] = game.xpath('td[@class="a3"]/strong/a/text()').extract()[0]
                item['comp'] = game.xpath('td[2]/text()').extract()[0]
                item['date'] = date
                item['mid'] = mid
                item['league'] = league
                item['team'] = team
                yield item

    def parse_game(self, response):
        try:
            jsonBody = json.loads(response.body_as_unicode())
            matchinfos = jsonBody['resultinfo']['matchinfo']
            player_home = jsonBody['resultinfo']['lineup']['home']['player']
            player_away = jsonBody['resultinfo']['lineup']['away']['player']
            stat = jsonBody['resultinfo']['stat']
            item = BTXItem()
            item['home'] = matchinfos['homename']
            item['away'] = matchinfos['awayname']
            item['comp'] = matchinfos['compname']
            item['date'] = matchinfos['datetime']
            item['mid'] = matchinfos['id']
            item['score'] = stat['homescore'] + ' - ' + stat['awayscore']
            item['possession'] = stat['home']['pp'] + '%' + ' - ' + stat['away']['pp'] + '%'
            item['passing'] = self.TS('p', stat)
            item['formation'] = self.TS('fm', stat)
            item['cross'] = self.TS('ap', stat)
            item['shoot'] = self.TS('s', stat)
            item['shot_on'] = self.TS('so', stat)
            item['tackle'] = self.TS('t', stat)
            item['corner'] = self.TS('c', stat)
            item['free_kick'] = self.TS('fk', stat)
            item['offside'] = self.TS('o', stat)
            item['foul'] = self.TS('f', stat)
            item['yel_card'] = self.TS('yb', stat)
            item['red_card'] = self.TS('rb', stat)
            item['game_time'] = stat['time']
            item['home_players'] = tuple({'player': x['name'], 'status': x['status']} for x in player_home)
            item['away_players'] = tuple({'player': x['name'], 'status': x['status']} for x in player_away)
            player = {x['id']: x['name'] for x in player_home}
            player.update({x['id']: x['name'] for x in player_away})
            home_goal = jsonBody['resultinfo']['goal']['home']
            item['home_goaler'] = tuple({'goaler': player[x['id']], 'time': x['time']} for x in home_goal['player']) if home_goal else 'None'
            away_goal = jsonBody['resultinfo']['goal']['away']
            item['away_goaler'] = tuple({'goaler': player[x['id']], 'time': x['time']} for x in away_goal['player']) if away_goal else 'None'
            yield item
        except:
            logging.info('data error: {}'.format(response.meta['mid']))

    def TS(self, tech, stat):
        try:
            home = stat['home']['{}'.format(tech)]
        except:
            home = '0'
        try:
            away = stat['away']['{}'.format(tech)]
        except:
            away = '0'
        return '{} - {}'.format(home, away)