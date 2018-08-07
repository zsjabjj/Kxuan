# -*- coding: utf-8 -*-
import datetime
import json
import logging
import random
import re

import scrapy

from Kxuan.MonthSellPC import request_detail
from Kxuan.pipelines import WasherPipeline
from Kxuan.settings import D_APPLIANCES, D_BRANDS_WASHER, D_NICKS, custom_settings_for_washer, MY_USER_AGENT, \
    WASHER_MODEL


class WasherSpider(scrapy.Spider):
    '''洗衣机'''
    # 管道
    # pipeline = set([WasherPipeline, ])
    pipeline = {WasherPipeline,}
    custom_settings = custom_settings_for_washer
    # 爬虫名
    name = 'washer'
    # url过滤
    allowed_domains = ['list.tmall.com', 'h5api.m.taobao.com', 'detail.m.tmall.com']
    # start_urls = ['http://tmall.com/']
    # 基础url
    base_url = 'https://list.tmall.com/m/search_items.htm?page_size=20&page_no={page_no}&q={q}&cat=54296792&brand={brand}'
    # # 构建型号列表
    washer_list = WASHER_MODEL.split(',')

    def start_requests(self):
        '''构建起始url'''
        # for q in D_APPLIANCES[0]:

        print(D_APPLIANCES[0])

        url = self.base_url.format(q=D_APPLIANCES[0], page_no=1, brand='')
        print(url)
        yield scrapy.Request(
            url,
            headers={
                'User-Agent': random.choice(MY_USER_AGENT),
            },
            meta={"device_category": D_APPLIANCES[0], "url": self.base_url},
        )

    def parse(self, response):
        '''解析起始url'''
        print(response.url)
        print(type(response.text))
        # with open('tmall.txt', 'w') as f:
        #     f.write(response.text)

        # 将json字符串转成json字典
        jsonp = json.loads(response.text)

        # 获取品牌ID(目前只获取TCL,Haier/海尔,Midea/美的,Sanyo/三洋,Littleswan/小天鹅, SIEMENS/西门子, Whirlpool/惠而浦, Royalstar/荣事达)
        brand_list = jsonp['brand_list']
        brandid_list = [str(brand['brand_id']) for brand in brand_list if brand['brand_name'] in D_BRANDS_WASHER]
        # print(brandid_list)
        # 手动添加荣事达品牌ID

        brandid_list.append('30654')


        # 重新拼接url
        new_url = response.meta['url'].format(q=response.meta['device_category'], page_no=1, brand=','.join(brandid_list))

        print('new_url:', new_url)
        # url = new_url + '&brand=' + ','.join(brandid_list)
        # print('shuju:' + url)
        # response.meta['url'] = new_url
        response.meta['brand'] = ','.join(brandid_list)
        response.meta['page_no'] = 1

        # 发请求获取五个品牌数据
        yield scrapy.Request(
            new_url,
            headers={
                'User-Agent': random.choice(MY_USER_AGENT),
            },
            callback=self.parse_item,
            meta=response.meta,
        )

    def parse_item(self, response):
        '''解析8个品牌数据'''
        print(response.url)
        print(response.meta)

        # 将json字符串转成json字典
        jsonp = json.loads(response.text)

        '''
        # 天猫商品: 洗衣机，冰箱
        # --商品类别: device_category
        # --商品ID: item_nid
        # 商品标题: item_title
        # --月销量(列表页): month_sold_list
        # 月销量(详情页): month_sold_detail
        # 图片链接: pic_url
        # 产品类型: category
        # 容量段: capacity
        # 型号: model
        # 品牌: brand
        # --店铺: nick
        # --页面价: item_price
        # 到手价: hand_price
        # 活动: activity
        # 玩法，pic_url: offer
        # --详情页链接: detail_url
        # 制冷方式 冰箱: fridge_method
        # 能效 冰箱: efficiency
        '''
        if jsonp['item']:
            response.meta['page_no'] += 1
            # item_list = jsonp['item']

            item_list = [item for item in jsonp['item'] if item['shop_name'] in D_NICKS]



            for item in item_list:
                if '冰箱' in item['title'] and '洗衣机' in item['title']:
                    pass
                else:
                    item_dict = dict()
                    item_dict['device_category'] = response.meta['device_category']
                    item_dict['item_nid'] = item['item_id']
                    item_dict['item_price'] = item['price']
                    item_dict['nick'] = item['shop_name']
                    # item_dict['item_title'] = item['title'].split(' ')[1]
                    item_dict['item_title'] = item['title']
                    item_dict['detail_url'] = item['url']
                    item_dict['month_sold_list'] = item['sold']
                    # item_dict['url'] = response.meta['url']
                    # item_dict['brand'] = response.meta['brand']
                    data = '%7B"itemNumId"%3A"{nid}"%7D'.format(nid=item['item_id'])

                    # https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp3&data=%7B%22itemNumId%22%3A%22537689688538%22%7D
                    # 构建详情页数据url
                    new_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp3&data={data}'.format(data=data)
                    print(new_url)
                    yield scrapy.Request(
                        new_url,
                        headers={
                            'User-Agent': random.choice(MY_USER_AGENT),
                        },
                        callback=self.parse_detail,
                        meta=item_dict,
                    )

            # 下一页
            next_url = response.meta['url'].format(q=response.meta['device_category'], brand=response.meta['brand'], page_no=response.meta['page_no'])

            yield scrapy.Request(
                next_url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                },
                callback=self.parse_item,
                meta=response.meta
            )

        # 将剩下的型号商品获取齐全
        elif self.washer_list:
            print('lackModelUrl------>', self.washer_list)
            for model in self.washer_list:
                lackModelUrl = response.meta['url'].format(q=response.meta['device_category'] + model, page_no=1, brand='')
                yield scrapy.Request(
                    lackModelUrl,
                    callback=self.parse_item,
                    meta=response.meta
                )


    def parse_detail(self, response):
        '''获取详情页中商品详细信息'''
        data = response.meta
        print('detail_url:%s' % response.url)
        # print(response.meta)

        # 详情页源码获取月销量
        sell_count = request_detail(data)
        print('sell_count----------:', sell_count)

        # 提取详情页数据
        data_detail = re.findall(r'mtopjsonp3\((.*)\)', response.body.decode())[0]
        data_count = json.loads(data_detail)['data']
        detail_list = data_count['props']['groupProps'][0]['基本信息']
        # print()
        # print('详细列表:%s' % data_count['props']['groupProps'][0]['基本信息'])
        # print('title:%s\npic_url:%s' % (data_count['item']['title'], data_count['item']['images'][0]))

        # 进一步提取有用数据
        print('详情页月销量:', re.findall(r'"sellCount":"(.*?)"', data_count['apiStack'][0]['value']))
        try:
            sellCount = re.findall(r'"sellCount":"(.*?)"', data_count['apiStack'][0]['value'])[0]
        except:
            logging.error('月销量title:%s' % data['item_title'])
            print('sellCount --------- error')
            sellCount = sell_count
            print('sellCount --------- error:', sell_count)
            # with open('./tmall/washer_%s_%s.txt' % (datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), data['item_nid']), 'w') as f:
            #     f.write(data_count)

        # 数据存储
        item = dict()
        # --商品类别: device_category
        item['device_category'] = data['device_category']
        for info in detail_list:
            # 产品类型: category
            if '产品类型' in info:
                item['category'] = info['产品类型'].strip()
            # 容量段: capacity
            elif '洗涤公斤量' in info:
                capacity = re.findall(r'(.*)kg', info['洗涤公斤量'].strip())[0]
                if '.' in capacity and capacity.split('.')[1] == '0':
                    item['capacity'] = capacity.split('.')[0]
                else:
                    item['capacity'] = capacity
            # 型号: model
            elif '型号' in info:
                item['model'] = info['型号'].strip()
            elif '海尔洗衣机型号' in info:
                item['model'] = info['海尔洗衣机型号'].strip()
            elif '三洋洗衣机型号' in info:
                item['model'] = info['三洋洗衣机型号'].strip()
            elif '荣事达洗衣机型号' in info:
                item['model'] = info['荣事达洗衣机型号'].strip()
            # 品牌: brand
            elif '洗衣机品牌' in info:
                item['brand'] = info['洗衣机品牌'].strip()
        # 到手价: hand_price
        # item['hand_price'] = '待处理,目前需手动获取'
        item['hand_price'] = ''
        # 活动: activity
        # item['activity'] = '待处理,目前需手动获取'
        item['activity'] = ''
        # 玩法，pic_url: offer
        # item['offer'] = '待处理,目前需手动获取'
        item['offer'] = ''
        # --页面价: item_price
        item['item_price'] = data['item_price']
        # --月销量(列表页): month_sold_list
        item['month_sold_list'] = data['month_sold_list']
        # 月销量(详情页): month_sold_detail
        item['month_sold_detail'] = sellCount
        # 商品标题: item_title
        item['item_title'] = data_count['item']['title']
        # --详情页链接: detail_url
        item['detail_url'] = 'https:' + data['detail_url']
        # 图片链接: pic_url
        item['pic_url'] = 'https:' + data_count['item']['images'][0]
        # --商品ID: item_nid
        item['item_nid'] = data['item_nid']
        # --店铺: nick
        item['nick'] = data['nick']
        # 制冷方式 冰箱: fridge_method
        # item['fridge_method'] = None
        # 能效 冰箱: efficiency
        # item['efficiency'] = None

        # fridge_list = FRIDGE_MODEL.split(',')
        if item['model'] in self.washer_list:
            # #
            self.washer_list.pop(self.washer_list.index(item['model']))
            print('washer model list===============>', self.washer_list)

        yield item











