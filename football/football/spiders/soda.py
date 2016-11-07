# -*- coding: utf-8 -*-
import scrapy
import logging
import pymongo
from scrapy.http import Request
from football.items import ASodaItem, BSodaItem


class SodaSpider(scrapy.Spider):
    name = "soda"
    allowed_domains = ["sodasoccer.com"]
    start_urls = (
        'http://www.sodasoccer.com/dasai/index.html',
    )
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.sodasoccer.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
        },
        'ITEM_PIPELINES': {
            'football.pipelines.SodaPipeline': 100,
        }
    }

    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.post = client['FOOTBALL']['hash-soda']
        self.client = client

    def parse(self, response):  # 爬取所有联赛的资料
        leagues = response.xpath('//div[@class="league_box1"][position()>1]/ul/li/div/a/@href').extract()
        for league in leagues:
            link = response.urljoin(league)
            yield Request(link, callback=self.parse_league)

    # def start_requests(self):  #爬取个别联赛的资料 133:英超， 100:意甲， 45:西甲， 115:德甲， 122:法甲， 282:中超
    #     nums = (133, 100, 45, 115, 122, 282,)
    #     header = {
    #         'Referer': 'http://www.sodasoccer.com/dasai/index.html',
    #     }
    #     for num in nums:
    #         link = 'http://www.sodasoccer.com/dasai/league/{}.html'.format(num)
    #         yield Request(link, callback=self.parse_league, headers=header)

    def parse_league(self, response):  #联赛资料
        for club in response.xpath('//ul[@class="lyul2"]/li/a'):
            link = club.xpath('@href').extract()[0]
            link = response.urljoin(link)
            yield Request(link, callback=self.parse_team)

    def parse_team(self, response):  #球队资料
        team = response.xpath('//h1[@class="headtip"]/text()').extract()[0]
        logging.info('{}'.format(team))
        for game in response.xpath('//div[re:match(@id, "match_\d")]/table/tr[@id]'):
            if game.xpath('td[5]/text()').extract()[0] != '-:-':
                home_away = game.xpath('@id').re('list_(\w+)')[0]
                date = game.xpath('td[1]/text()').extract()[0]
                score = game.xpath('td[5]/text()').extract()[0]
                match = game.xpath('td[4]/a/text()').extract()[0]
                comp = game.xpath('td[2]/text()').extract()[0]
                goal = game.xpath('td[last()]/@title').extract()[0]
                link = game.xpath('td[last()-1]/span/a/@href').extract()[0]
                link = response.urljoin(link)
                yield Request(link, callback=self.parse_page, meta={
                                                                    'team': team,
                                                                    'home_away': home_away,
                                                                    'score': score,
                                                                    'date': date,
                                                                    'match': match,
                                                                    'comp': comp,
                                                                    'goal': goal,
                                                                    })

    def parse_page(self, response):  #比赛页面，获取json的接口地址
        team = response.meta['team']
        home_away = response.meta['home_away']
        score = response.meta['score']
        date = response.meta['date']
        match = response.meta['match']
        comp = response.meta['comp']
        goal = response.meta['goal']
        mid = response.xpath('//script').re('return  (\d+)')[0]
        if self.post.find_one({'mid': mid}) == None:
            link = 'http://www.sodasoccer.com/dasai/xml/{}.xml'.format(mid)
            yield Request(link, callback=self.parse_game, meta={
                                                                'score': score,
                                                                'date': date,
                                                                'comp': comp,
                                                                'mid': mid,
                                                                })
        if self.client[comp][team].find_one({'_id': mid}) == None:
            item = ASodaItem()
            item['team'] = team
            item['home_away'] = home_away
            item['score'] = score
            item['date'] = date
            item['match'] = match
            item['comp'] = comp
            item['goal'] = goal
            item['mid'] = mid
            yield item

    def parse_game(self, response):  #获取比赛的分析统计
        item = BSodaItem()
        item['score'] = response.meta['score']
        item['date'] = response.meta['date']
        item['comp'] = response.meta['comp']
        item['mid'] = response.meta['mid']
        try:
            item['season'] = response.xpath('//comp_season/text()').extract()[0]
        except IndexError:
            item['season'] = '不详'
        try:
            item['referee'] = response.xpath('//main/text()').extract()[0]
        except IndexError:
            item['referee'] = '不详'
        try:
            item['round'] = '第 {} 轮'.format(response.xpath('//match_round/text()').extract()[0])
        except:
            item['round'] = 'None'
        home = response.xpath('//home')
        away = response.xpath('//away')
        item['formation'] = self.formation(response)
        item['teams'] = home.xpath('club_name/text()').extract()[0] + ' - ' + away.xpath('club_name/text()').extract()[0]
        item['shot_on'] = self.TS(response, 'ontarget_scoring_att')
        item['possession'] = self.TS(response, 'possession_percentage')
        item['cross'] = self.TS(response, 'total_cross')
        item['offside'] = self.TS(response, 'total_offside')
        item['passing'] = self.TS(response, 'total_pass')
        item['shoot'] = self.TS(response, 'total_scoring_att')
        item['tackle'] = self.TS(response, 'total_tackle')
        item['yel_card'] = self.TS(response, 'total_yel_card')
        item['corner'] = self.TS(response, 'won_corners')
        item['saves'] = self.TS(response, 'saves')
        item['red_card'] = self.TS(response, 'total_red_card')
        item['shot_post'] = self.TS(response, 'post_scoring_att')
        item['home_goaler'] = tuple({'Goaler': x.xpath('@name').extract()[0], 'Time': x.xpath('@time').extract()[0], 'Assi': x.xpath('@name_Assi').extract()[0]} for x in home.xpath('goal/player_goal'))
        item['away_goaler'] = tuple({'Goaler': x.xpath('@name').extract()[0], 'Time': x.xpath('@time').extract()[0], 'Assi': x.xpath('@name_Assi').extract()[0]} for x in away.xpath('goal/player_goal'))
        item['home_player'] = tuple({'Player': x.xpath('@player_name').extract()[0], 'Status': x.xpath('@player_status').extract()[0], 'Position': x.xpath('@player_position').extract()[0], 'Num': x.xpath('@player_number').extract()[0]} for x in home.xpath('club_list/player[position()<last()]'))
        item['away_player'] = tuple({'Player': x.xpath('@player_name').extract()[0], 'Status': x.xpath('@player_status').extract()[0], 'Position': x.xpath('@player_position').extract()[0], 'Num': x.xpath('@player_number').extract()[0]} for x in away.xpath('club_list/player[position()<last()]'))
        item['home_action'] = tuple({'Action': x.xpath('@action_name').extract()[0], 'Time': x.xpath('@action_time').extract()[0], 'Property': x.xpath('@property').extract()[0]} for x in home.xpath('club_affair_list/action'))
        item['away_action'] = tuple({'Action': x.xpath('@action_name').extract()[0], 'Time': x.xpath('@action_time').extract()[0], 'Property': x.xpath('@property').extract()[0]} for x in away.xpath('club_affair_list/action'))
        yield item

    def formation(self, response):
        try:
            home = response.xpath('//home/club_formation/text()').extract()[0]
        except:
            home = '不详'
        try:
            away = response.xpath('//away/club_formation/text()').extract()[0]
        except:
            away = '不详'
        return '{} - {}'.format(home, away)

    def TS(self, response, affair):
        try:
            home = response.xpath('//home/club_affair/{}/text()'.format(affair)).extract()[0]
        except:
            home = '0'
        try:
            away = response.xpath('//away/club_affair/{}/text()'.format(affair)).extract()[0]
        except:
            away = '0'
        return '{} - {}'.format(home, away)
