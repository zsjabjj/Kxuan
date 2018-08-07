# -*- coding: utf-8 -*-
import json
import logging
import re

import scrapy

from Kxuan.pipelines import TaobaoPipeline
from Kxuan.settings import custom_settings_for_taobao


class TaobaoSpider(scrapy.Spider):

    # 管道
    # pipeline = set([TmallPipeline, ])
    pipeline = {TaobaoPipeline, }
    custom_settings = custom_settings_for_taobao

    name = 'taobao'
    allowed_domains = ['s.taobao.com', 'h5api.m.taobao.com']
    # https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&callback=jsonp1257&q=%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%86%B0%E7%AE%B1&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180611&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44

    # start_urls = ['http://taobao.com/']
    base_url = 'https://s.taobao.com/search?data-key=s&data-value={data_value}&ajax=true&callback=jsonp&q=%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%86%B0%E7%AE%B1&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180611&ie=utf8&p4ppushleft=1%2C48&s={s}'

    num = 44

    def start_requests(self):
        '''构建初始url'''
        url = self.base_url.format(data_value='0%2C1', s=44)
        yield scrapy.Request(url)

    def parse(self, response):
        '''解析'''
        print('parse:', response.url)
        # 提取数据
        data_detail = re.findall(r'jsonp\((.*)\)', response.body.decode())[0]
        data_count = json.loads(data_detail)

        # item列表
        item_list = data_count['mods']['itemlist']['data']['auctions']
        # 页数
        currentPage = data_count['mods']['pager']['data']['currentPage']
        totalPage = data_count['mods']['pager']['data']['totalPage']


        if item_list:
            for item in item_list:
                item_dict = dict()
                item_dict['detail_url'] = 'https:' + item['detail_url']
                item_dict['nid'] = item['nid']
                item_dict['raw_title'] = item['raw_title']
                if 'p4p' in item:
                    print('p4p:', item['p4p'])
                    pass
                else:
                    # 天猫
                    if 'tmall' in item['detail_url']:
                        data = '%7B%22itemNumId%22%3A%22{}%22%7D'.format(item['nid'])
                        tmall_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&sign=81a1d05ef34af3c5bd319c8f0047c5b0&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=' + data
                        yield scrapy.Request(
                            tmall_url,
                            callback=self.parse_tmall,
                            meta=item_dict,
                        )
                    # 淘宝
                    elif 'taobao' in item['detail_url']:

                        data = '%7B%22exParams%22%3A%22%7B%5C%22spm%5C%22%3A%5C%22a230r.1.14.291.5865129ddn8wrT%5C%22%2C%5C%22id%5C%22%3A%5C%22{}%5C%22%2C%5C%22ns%5C%22%3A%5C%221%5C%22%2C%5C%22abbucket%5C%22%3A%5C%2210%5C%22%7D%22%2C%22itemNumId%22%3A%22{}%22%7D'.format(item['nid'], item['nid'])
                        taobao_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&sign=ece650d07c6993163a34e57a1e27aef3&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=' + data
                        yield scrapy.Request(
                            taobao_url,
                            callback=self.parse_taobao,
                            meta=item_dict,
                        )


        # else:
        #     pass
        print('currentPage:', currentPage, 'totalPage:', totalPage)
        if currentPage < totalPage:
            data_value = self.num * currentPage
            s = data_value - 44
            next_url = self.base_url.format(data_value=data_value, s=s)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )



    def parse_tmall(self, response):
        '''天猫数据'''
        # print('parse_tmall:', response.url)

        abc_sum = 0


        item = dict()

        data = response.meta
        try:
            item['detail_url'] = data['detail_url']
        except:
            logging.error(data['raw_title'])
        item['nid'] = data['nid']
        item['raw_title'] = data['raw_title']

        data_detail = re.findall(r'mtopjsonp2\((.*)\)', response.body.decode())[0]
        data_count = json.loads(data_detail)
        # 月销量
        sell_count = data_count['data']['apiStack'][0]['value']
        sellCount = re.findall(r'.*"sellCount":"(.*?)"', sell_count)
        try:
            item['sellCount'] = sellCount[0]
        except:
            item['sellCount'] = '手动抓取'
        # 图片链接
        item['img_url'] = 'http:' + data_count['data']['item']['images'][0]

        # 基本信息
        detail_list = data_count['data']['props']['groupProps'][0]['基本信息']
        for detail in detail_list:
            key_name = list(detail.keys())[0]
            if '品牌' in key_name:
                item['brand'] = detail[key_name].strip()
                abc_sum += 1

            elif '型号' in key_name:
                item['model'] = detail[key_name].strip()
                abc_sum += 1
            elif '西门子' in key_name:
                item['model'] = detail[key_name].strip()
                abc_sum += 1

            elif '澳柯玛' in key_name:
                item['model'] = detail[key_name].strip()
                abc_sum += 1
            elif '最大容积' in key_name:
                item['max_box'] = detail[key_name].strip()
                abc_sum += 1

            elif '箱门结构' in key_name:
                item['box_style'] = detail[key_name].strip()
                abc_sum += 1
                pass

            elif '宽×深(厚)×高' == key_name:
                item['box_size'] = detail[key_name].strip()
                abc_sum += 1
                pass

            elif '尺寸' == key_name:
                item['box_size'] = detail[key_name].strip()
                abc_sum += 1
                pass

            if 5 == abc_sum:
                break
        print('abc_sum_tmall:', abc_sum)
        print('tmall:', item)
        try:
            box_deep = re.findall(r'.*x(.*)x.*mm', item['box_size'])[0]
        except:
            logging.error(response.url)
        else:

            if int(box_deep) < 700:
                yield item



    def parse_taobao(self, response):
        '''淘宝数据'''
        # print('parse_taobao:', response.url)
        abc_sum = 0

        item = dict()

        data = response.meta
        item['detail_url'] = data['detail_url']
        item['nid'] = data['nid']
        item['raw_title'] = data['raw_title']

        data_detail = re.findall(r'mtopjsonp1\((.*)\)', response.body.decode())[0]
        data_count = json.loads(data_detail)
        # 月销量
        sell_count = data_count['data']['apiStack'][0]['value']
        sellCount = re.findall(r'.*"sellCount":"(.*?)"', sell_count)
        try:
            item['sellCount'] = sellCount[0]
        except:
            item['sellCount'] = '手动抓取'
        # 图片链接
        item['img_url'] = 'http:' + data_count['data']['item']['images'][0]

        # 基本信息
        detail_list = data_count['data']['props']['groupProps'][0]['基本信息']
        for detail in detail_list:
            key_name = list(detail.keys())[0]
            if '品牌' in key_name:
                item['brand'] = detail[key_name]
                abc_sum += 1

            elif '型号' in key_name:
                item['model'] = detail[key_name]
                abc_sum += 1

            elif '西门子' in key_name:
                item['model'] = detail[key_name].strip()
                abc_sum += 1
            elif '澳柯玛' in key_name:
                item['model'] = detail[key_name].strip()
                abc_sum += 1
            elif '最大容积' in key_name:
                item['max_box'] = detail[key_name]
                abc_sum += 1
            elif '箱门结构' in key_name:
                item['box_style'] = detail[key_name]
                abc_sum += 1
                pass
            elif '宽×深(厚)×高' == key_name:
                item['box_size'] = detail[key_name].strip()
                abc_sum += 1
                pass

            elif '尺寸' == key_name:
                item['box_size'] = detail[key_name].strip()
                abc_sum += 1
                pass


            if 5 == abc_sum:
                break
        print('abc_sum_taobao:', abc_sum)
        print('taobao:', item)
        try:
            box_deep = re.findall(r'.*x(.*)x.*mm', item['box_size'])[0]


        except:
            logging.error(response.url)
        else:
            if int(box_deep) < 700:
                yield item

