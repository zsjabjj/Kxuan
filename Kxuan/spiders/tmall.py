# -*- coding: utf-8 -*-
import datetime
import io
import json
import logging
import random
import re
import sys
import time
from selenium import webdriver

import requests
import scrapy
from lxml import etree
from selenium.webdriver import DesiredCapabilities
from Kxuan.MonthSellPC import Fire
# from Kxuan.MonthSellPC import request_detail
from Kxuan.pipelines import TmallPipeline
from Kxuan.settings import DEVICE_CATEGORY, BRANDS, custom_settings_for_tmall, MY_USER_AGENT_PC, MY_USER_AGENT, NOT_LIST

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RiceTmallSpider(scrapy.Spider):
    '''天猫超市小家电'''
    # 管道
    # pipeline = set([TmallPipeline, ])
    pipeline = {TmallPipeline,}
    custom_settings = custom_settings_for_tmall
    # 爬虫名
    name = 'tmall'
    # url过滤
    allowed_domains = ['list.tmall.com', 'h5api.m.taobao.com', 'detail.m.tmall.com']
    # start_urls = ['http://tmall.com/']
    # 基础url
    base_url = 'https://list.tmall.com/chaoshi_data.htm?user_id=725677994&q={q}&unify=yes&from=chaoshi&p={p}&brand={brand}&cat=50514008'
    baseImgUrl = 'https://list.tmall.com/m/search_items.htm?page_size=20&page_no={page_no}&q={q}&type=p&tmhkh5=&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_searchbutton&sort=d&cat={catId}'
    # 销量：https://list.tmall.com/m/search_items.htm?page_size=20&page_no=1&q=MB-WFS5017TM&type=p&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_searchbutton&sort=d
    baseUrlcg = 'https://list.tmall.com/chaoshi_data.htm?p={p}&user_id=725677994&q={q}&cat=50514008&brand={brand}&unify=yes&from=chaoshi'

    line_list = [line.strip() for line in open('./model.txt') if line]


    def start_requests(self):
        '''构建起始url'''
        for q in DEVICE_CATEGORY:

            url = self.base_url.format(q=q, p=1, brand='')
            yield scrapy.Request(
                url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                    # 'Referer': 'https://sec.taobao.com/query.htm?smApp=tmallsearch&smPolicy=tmallsearch-product-anti_Spider-html-checkcode&smCharset=GBK&smTag=MTEyLjE3Ljk1LjI0MywsYjZmYTIxNzVmNGMxNDIzZmE5NmJhOGI1OGE5NjQ1ODQ%3D&smReturn=https%3A%2F%2Flist.tmall.com%2Fsearch_product.htm%3Fspm%3Da3204.7933263.0.0.781f173fzlv4ue%26cat%3D50514008%26brand%3D30652%2C30850%2C30844%2C31358%26q%3D%25B5%25E7%25B4%25C5%25C2%25AF%26sort%3Dwd%26style%3Dg%26user_id%3D725677994%2C1910146537%2C2136152958%26active%3D1%26industryCatId%3D50514008%26smAreaId%3D330100&smSign=U%2F%2BU%2FhNonUIXLW67v8Zm1Q%3D%3D&captcha=https%3A%2F%2Fsec.taobao.com%2Fquery.htm',
                },
                meta={"device_category": q, "url": self.base_url},
            )

        for line in self.line_list:
            if 'MP-WCT30A02' == line or 'CL32T1' == line or 'MJ-LZ25Easy203' == line:
                jp_url = self.baseImgUrl.format(page_no=1, q=line, catId='')
            else:
                # self.line_list.pop(self.line_list.index(line))
                jp_url = self.baseImgUrl.format(page_no=1, q=line, catId=54312951)
            num = 1
            again = 1

            yield scrapy.Request(
                jp_url,
                callback=self.parse_jp,
                meta={'model': line, 'num': num, 'again': again},
            )

    def parse(self, response):
        '''解析起始url'''

        # 将json字符串转成json字典
        # print(response.content.decode('utf-8'))

        jsonp = json.loads(response.text)

        # 获取品牌ID(目前只获取九阳，美的，苏泊尔)
        brand_list = jsonp['nav']['brand']['brandList']
        # brandid_list = [str(brand['id']) for brand in brand_list if brand['name'] in BRANDS]
        brandid_list = [str(brand['id']) for brand in brand_list]
        # brandname_list = ','.join([brand['name'] for brand in brand_list])
        # print(brandid_list)

        # 类目选为家用电器
        cat_list = jsonp['nav']['cat']['subCatList']
        try:
            catId = [str(cat['catId']) for cat in cat_list if cat['name'] == '家用电器'][0]
        except:
            catId = ''

        # 重新拼接url
        new_url = response.meta['url'].format(q=response.meta['device_category'], p=1, brand=','.join(brandid_list))
        baseUrl = re.sub(r'cat=(.*)', r'cat=' + catId, response.meta['url'])
        url = re.sub(r'cat=(.*)', r'cat=' + catId, new_url)

        response.meta['url'] = baseUrl
        response.meta['brandid'] = ','.join(brandid_list)
        # response.meta['brandname_list'] = brandname_list
        if '炒锅' == response.meta['device_category']:
            yield scrapy.Request(
                new_url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                },
                callback=self.parse_item,
                meta=response.meta,
            )
        else:
            # 发请求获取三个品牌数据
            yield scrapy.Request(
                url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                },
                callback=self.parse_item,
                meta=response.meta,
            )

    def parse_item(self, response):
        '''解析三个品牌数据'''

        # 将json字符串转成json字典
        jsonp = json.loads(response.text)

        # 获取页数
        # 当前页
        curPage = jsonp['page']['curPage']
        # 每页数量
        totalNum = jsonp['page']['totalNum']
        # 总页数
        totalPage = jsonp['page']['totalPage']

        # 提取数据
        for item in jsonp['srp']:
            item_dict = dict()
            item_dict['device_category'] = response.meta['device_category']
            item_dict['item_price'] = item['price']
            item_dict['month_sold_list'] = item['sold']
            item_dict['item_title'] = item['title']
            item_dict['detail_url'] = 'https:' + item['url']
            item_dict['pic_url'] = 'https:' + item['img']
            item_dict['item_nid'] = item['nid']
            item_dict['reserve_price'] = item['reservePrice']
            item_dict['post_fee'] = item['postFee']
            item_dict['totalPage'] = totalPage
            item_dict['curPage'] = curPage
            item_dict['url'] = response.meta['url']
            item_dict['brandid'] = response.meta['brandid']
            # item_dict['brandname_list'] = response.meta['brandname_list']
            # data = {"itemNumId": str(item['nid'])}
            data = '%7B"itemNumId"%3A"{}"%7D'.format(item['nid'])
            # data_str = json.dumps(data, ensure_ascii=False)

            new_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp3&data=' + data

            yield scrapy.Request(
                new_url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                },
                callback=self.parse_detail,
                meta=item_dict,
            )

    def parse_detail(self, response):
        '''获取促销'''
        # time.sleep(0.5)
        data = response.meta

        # 详情页源码获取月销量
        # sell_count = request_detail(data)
        sell_count = Fire().get_sell(data)
        # print('sell_count----------:', sell_count)

        # 获取API的数据
        data_detail = re.findall(r'mtopjsonp3\((.*)\)', response.body.decode())[0]

        # logging.info('data_detail length: %s' % len(data_detail))
        try:
            data_count = json.loads(data_detail)['data']['apiStack'][0]['value']
        except:
            logging.error(data_detail)
        detail_list = json.loads(data_detail)['data']['props']['groupProps'][0]['基本信息']

        try:
            sellCount = re.findall(r'"sellCount":"(.*?)"', data_count)[0]
        except Exception as err:
            logging.error('月销量title:%s' % data['item_title'])
            sellCount = sell_count


        item = dict()
        item['device_category'] = data['device_category']
        for info in detail_list:
            # 品牌: brand
            if '品牌' in info:
                item['brand'] = info['品牌'].strip()

            elif '电磁炉品牌' in info:
                item['brand'] = info['电磁炉品牌'].strip()
            elif '电热水壶品牌' in info:
                item['brand'] = info['电热水壶品牌'].strip()
            elif '咖啡机品牌' in info:
                item['brand'] = info['咖啡机品牌'].strip()
            # 型号: model
            elif '型号' in info:
                item['model'] = info['型号'].strip()
            elif ' 型号' in info:
                item['model'] = info[' 型号'].strip()
            elif '九阳榨汁机型号' in info:
                item['model'] = info['九阳榨汁机型号'].strip()
            elif '美的榨汁搅拌料理机型号' in info:
                item['model'] = info['美的榨汁搅拌料理机型号'].strip()
            elif '九阳豆浆机型号' in info:
                item['model'] = info['九阳豆浆机型号'].strip()
            elif '美的豆浆机型号' in info:
                item['model'] = info['美的豆浆机型号'].strip()
            elif '小熊酸奶机型号' in info:
                item['model'] = info['小熊酸奶机型号'].strip()
            elif '美的面包机型号' in info:
                item['model'] = info['美的面包机型号'].strip()
            elif '小熊煮蛋器型号' in info:
                item['model'] = info['小熊煮蛋器型号'].strip()

        item['item_price'] = data['item_price']
        item['month_sold_list'] = data['month_sold_list']
        item['month_sold_detail'] = sellCount
        item['item_title'] = data['item_title']
        item['detail_url'] = data['detail_url']
        # item['pic_url'] = data['pic_url']
        item['pic_url'] = re.match(r'(.*)_100x100.jpg', data['pic_url']).group(1)
        item['item_nid'] = data['item_nid']
        item['reserve_price'] = data['reserve_price']
        item['post_fee'] = data['post_fee']
        item['url'] = data['url']
        item['brandid'] = data['brandid']
        # item['brandname_list'] = data['brandname_list']

        item_price = item['item_price'].split('.')[0]
        item_price_point = item['item_price'].split('.')[1]

        # 判断详情页中是否有促销
        if '促销' in data_count:
            # logging.info('促销: %s' % response.url)
            # "content":["满1件,打8折"],"iconText":"促销"
            # logging.info('促销活动: %s' % re.findall(r'"content":\["(.*?)"\]', data_count))


            try:

                full, less = re.findall(r'满(\d+?)元,省(\d+?)元', data_count)[0]
                # logging.info('满减 %s %s' % (full, less))

                if int(full) <= int(item_price):
                    item['hand_price'] = str(int(item_price) - int(less)) + '.' + item_price_point
                else:
                    item['hand_price'] = '满%s元,省%s元' % (full, less)

            except:
                try:
                    full, less = re.findall(r'满(\d+?)件,打(\d+?)折', data_count)[0]
                    # logging.info('满折 %s %s %s' % (full, less, type(full)))
                    if '1' == full:

                        item['hand_price'] = round(int(''.join(item['item_price'].split('.'))) * int(less) / 1000, 2)
                        # logging.info('hand_price: %s' % item['hand_price'])
                    else:
                        item['hand_price'] = '满%s件,打%s折' % (full, less)
                except:
                    item['hand_price'] = ''.join(re.findall(r'"content":\["(.*?)"\]', data_count))


        else:
            # logging.info('无促销')
            item['hand_price'] = item['item_price']

        if '电饼铛' == data['device_category']:
            week_url = 'https://list.tmall.com/search_product.htm?cat=50514008&brand=149474648,30652,30844,31358,30850&q={q}&sort=wd&style=g&user_id=725677994,1910146537,2136152958&industryCatId=50514008&smAreaId=330100'

        else:
            week_url = 'https://list.tmall.com/search_product.htm?cat=50514008&brand=30652,30850,30844,31358&q={q}&sort=wd&style=g&user_id=725677994,1910146537,2136152958&industryCatId=50514008&smAreaId=330100'

        yield scrapy.Request(
            week_url.format(q=data['device_category']),
            headers={
                'User-Agent': random.choice(MY_USER_AGENT_PC),
                # 'Referer': 'https://sec.taobao.com/query.htm?smApp=tmallsearch&smPolicy=tmallsearch-product-anti_Spider-html-checkcode&smCharset=GBK&smTag=MTEyLjE3Ljk1LjI0MywsYjZmYTIxNzVmNGMxNDIzZmE5NmJhOGI1OGE5NjQ1ODQ%3D&smReturn=https%3A%2F%2Flist.tmall.com%2Fsearch_product.htm%3Fspm%3Da3204.7933263.0.0.781f173fzlv4ue%26cat%3D50514008%26brand%3D30652%2C30850%2C30844%2C31358%26q%3D%25B5%25E7%25B4%25C5%25C2%25AF%26sort%3Dwd%26style%3Dg%26user_id%3D725677994%2C1910146537%2C2136152958%26active%3D1%26industryCatId%3D50514008%26smAreaId%3D330100&smSign=U%2F%2BU%2FhNonUIXLW67v8Zm1Q%3D%3D&captcha=https%3A%2F%2Fsec.taobao.com%2Fquery.htm',
            },
            callback=self.parse_pc_detail,
            dont_filter=True,
            meta=item,
        )





        # 构建翻页
        if data['curPage'] < data['totalPage']:
            # logging.info('curPage:%s < totalPage:%s' % (data['curPage'], data['totalPage']))
            # next_url = re.sub(r'p=(.*)', r'p=' + str(data['curPage'] + 1), data['url'])
            # https://list.tmall.com/chaoshi_data.htm?user_id=725677994&q={}&unify=yes&from=chaoshi&p={}&brand={}&cat=50514008
            next_url = data['url'].format(q=data['device_category'], p=str(data['curPage'] + 1), brand=data['brandid'])
            # logging.info('next_url: %s' % next_url)
            yield scrapy.Request(
                next_url,
                headers={
                    'User-Agent': random.choice(MY_USER_AGENT),
                },
                callback=self.parse_item,
                meta=item,
            )



    # def parse_pc_detail(self, url):
    def parse_pc_detail(self, response):
        '''获取商品周销量数据'''

        # print('======++++++======\n', response.text)
        data = response.meta
        item = dict()
        item['device_category'] = data['device_category']
        item['item_price'] = data['item_price']
        item['month_sold_list'] = data['month_sold_list']
        item['month_sold_detail'] = data['month_sold_detail']
        item['item_title'] = data['item_title']
        item['detail_url'] = data['detail_url']
        # item['pic_url'] = data['pic_url']
        item['pic_url'] = data['pic_url']
        item['item_nid'] = data['item_nid']
        item['reserve_price'] = data['reserve_price']
        item['post_fee'] = data['post_fee']
        item['hand_price'] = data['hand_price']
        try:
            # logging.info(data['brand'])
            item['brand'] = data['brand'].split('/')[1]
        except:
            item['brand'] = data['brand']
        item['model'] = data['model']

        # 格式化源码
        html = etree.HTML(response.text)

        i = 1
        # 获取商品标题和周销量  (存入列表，格式：{"<商品标题>":"<周销量>"})
        while True:
            # data_dict = dict()
            titles = html.xpath('//*[@id="J_ProductList"]/li[{}]/div/h3/a/text()|//*[@id="J_ProductList"]/li[{}]/div/h3/a/span/text()'.format(i, i))
            solds = html.xpath('//*[@id="J_ProductList"]/li[{}]/div/div[2]/div[1]/span/text()|//*[@id="J_ProductList"]/li[{}]/div/div[2]/div[1]/strong/text()'.format(i, i))

            # 判断此标签是否获取到标题
            if titles:
                # 过滤标题列表生成新的列表
                title_list = list()
                # title_list = [title.strip() for title in titles if titles.index(title) == 1 or -1]
                for title in titles:
                    if titles.index(title) == 0:
                        title = title.lstrip()

                    elif titles.index(title) == len(titles) - 1:
                        title = title.rstrip()
                    title_list.append(title)
                # print('title_list: %s' % title_list)
                # 将列表拼接成标题字符串
                t = ''.join(title_list)

                # 判断手机端商品标题是否和pc端标题一致
                if data['item_title'] in t:

                    try:
                        item['week_sold'] = solds[1]
                    except Exception as e:
                        logging.error(data['item_title'])
                        item['week_sold'] = 0
                    break

                i += 1

            else:
                break
        # 判断周销量是否已经获得
        if 'week_sold' in item:
            print('商品标题:%s' % (data['item_title']))
            print('week_sold:%s' % item['week_sold'])
            yield item

        # 没有获取到，下一页继续查找
        else:
            # 获取下一页链接
            page_next = html.xpath('//*[@id="content"]//a[@class="next-page"]/text()')
            nextUrls = html.xpath('//*[@id="content"]//a[@class="next-page"]/@href')

            if page_next:
                next_url = 'https://list.tmall.com/search_product.htm' + nextUrls[0]
                yield scrapy.Request(
                    next_url,
                    headers={
                        'User-Agent': random.choice(MY_USER_AGENT_PC),
                    },
                    callback=self.parse_pc_detail,
                    dont_filter=True,
                    meta=item,
                )
            else:
                logging.error('周销量出问题商品标题：%s' % data['item_title'])
                logging.error(response.url)
                logging.error('周销量出问题商品标题list：%s' % titles)

                item['week_sold'] = '待定...'

                yield item


    def parse_jp(self, response):
        '''获取竞品型号图片'''

        jsonp = json.loads(response.text)
        item_list = jsonp['item']
        current_page = jsonp['current_page']
        total_page = jsonp['total_page']

        if current_page == total_page and response.meta['again'] == 1:
            response.meta['num'] = 1

        if item_list:
            for item in item_list:
                item_dict = dict()
                item_dict['item_id'] = item['item_id']
                item_dict['shop_name'] = item['shop_name']
                # item_dict['image_urls'] = 'http:' + item['img']
                item_dict['model'] = response.meta['model']
                item_dict['num'] = response.meta['num']
                item_dict['current_page'] = current_page
                item_dict['total_page'] = total_page
                item_dict['item_price'] = item['price']
                item_dict['month_sold_list'] = item['sold']
                try:
                    title = item['title']
                except:
                    title = ''
                    logging.error(item)
                try:
                    price = item['price'].split('.')[0]
                except:
                    price = item['price']

                response.meta['num'] += 1
                item_dict['again'] = response.meta['again']

                data = '%7B"itemNumId"%3A"{}"%7D'.format(item['item_id'])

                new_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=' + data

                a = False
                for nok in NOT_LIST:
                    if nok in title:
                        a = True
                        break

                if not a and response.meta['num'] <= 6:
                    yield scrapy.Request(
                        new_url,
                        # headers={
                        #     'User-Agent': random.choice(MY_USER_AGENT),
                        # },
                        callback=self.parse_jpdetail,
                        meta=item_dict,
                    )
                else:
                    response.meta['num'] -= 1

        # 构建翻页
        if current_page < total_page:
            # logging.info('current_page:%s < total_page:%s' % (current_page, total_page))

            if 'MP-WCT30A02' == response.meta['model'] or 'CL32T1' == response.meta['model'] or 'MJ-LZ25Easy203' == response.meta['model']:
                next_url = self.baseImgUrl.format(q=response.meta['model'], page_no=str(current_page + 1), catId='')
            else:
                next_url = self.baseImgUrl.format(q=response.meta['model'], page_no=str(current_page + 1), catId=54312951)
            # logging.info('next_url: %s' % next_url)
            response.meta['again'] += 1
            yield scrapy.Request(
                next_url,
                # headers={
                #     'User-Agent': random.choice(MY_USER_AGENT),
                # },
                callback=self.parse_jp,
                meta=response.meta,
            )

        pass


    def parse_jpdetail(self, response):

        data = response.meta

        # http://img.alicdn.com/imgextra/i3/3253843559/TB2f82fh2iSBuNkSnhJXXbDcpXa_!!3253843559.jpg

        # 获取API的数据
        data_detail = re.findall(r'mtopjsonp2\((.*)\)', response.body.decode())[0]
        try:
            images = json.loads(data_detail)['data']['item']['images']
        except:
            images = list()
            logging.error(data_detail)

        item = dict()
        if images:
            img_url = 'http:' + images[0]

            item['item_id'] = data['item_id']
            item['shop_name'] = data['shop_name']
            # item['image_urls'] = data['image_urls']
            item['model'] = data['model']
            item['num'] = data['num']
            item['image_urls'] = img_url
            # item['current_page'] = current_page
            # item['total_page'] = total_page
            item['item_price'] = data['item_price']
            item['month_sold_list'] = data['month_sold_list']

            if item['num'] <= 5:
                # logging.info('img title: %s' % item['shop_name'])
                yield item
 











