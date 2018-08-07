# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KxuanItem(scrapy.Item):
    '''快选上的数据item'''
    '''
    self.item_kid = item_kid
    self.item_nid = item_nid
    self.item_pid = item_pid
    self.item_raw_title = item_raw_title
    self.item_title = item_title
    self.seller_id = seller_id
    self.seller_nick_name = seller_nick_name
    self.item_loc = item_loc
    self.detail_url = detail_url
    self.view_price =  view_price
    self.pic_url = pic_url
    self.comment_count = comment_count
    self.view_sales = view_sales
    self.shopLink = shopLink
    self.q_score = q_score
    self.category = category
    self.nick = nick
    

    '''
    # 天猫超市商品item：['电饭煲', '电炖锅', '电饼铛', '电压力锅', '养生壶', '电磁炉', '电热水壶', '料理机', '豆浆机', '电茶壶', '榨汁机', '电动打蛋机', '酸奶机', '面条机', '咖啡机']
    # 商品类别
    device_category = scrapy.Field()
    # item_kid
    item_kid = scrapy.Field()
    # item_nid
    item_nid = scrapy.Field()
    # item_pid
    item_pid = scrapy.Field()
    # item_vid
    item_vid = scrapy.Field()
    # item_raw_title
    item_raw_title = scrapy.Field()
    # item_title
    item_title = scrapy.Field()
    # seller_id
    seller_id = scrapy.Field()
    # seller_nick_name
    seller_nick_name = scrapy.Field()
    # item_loc
    item_loc = scrapy.Field()
    # detail_url
    detail_url = scrapy.Field()
    # view_price
    view_price = scrapy.Field()
    # pic_url
    pic_url = scrapy.Field()
    # comment_count
    comment_count = scrapy.Field()
    # view_sales
    view_sales = scrapy.Field()
    # shopLink, 存储前需要对store替换为店铺拼音的处理
    shopLink = scrapy.Field()
    # q_score
    q_score = scrapy.Field()
    # category
    category = scrapy.Field()
    # nick
    nick = scrapy.Field()
    # 标价
    item_price = scrapy.Field()
    # 到手价
    hand_price = scrapy.Field()
    # 月销量(列表页)
    month_sold_list = scrapy.Field()
    # 月销量(详情页)
    month_sold_detail = scrapy.Field()
    # 原价
    reserve_price = scrapy.Field()
    # 运费
    post_fee = scrapy.Field()
    # 周销量
    week_sold = scrapy.Field()

    # 天猫商品: 洗衣机，冰箱
    # 日期
    # date_time = scrapy.Field()
    # 产品类型
    # category
    # 容量段
    capacity = scrapy.Field()
    # 型号
    model = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 页面价
    # item_price
    # 到手价
    # hand_price
    # 活动
    activity = scrapy.Field()
    # 玩法，pic_url
    offer = scrapy.Field()
    # 详情页链接
    # detail_url
    # 制冷方式 冰箱
    fridge_method = scrapy.Field()
    # 能效 冰箱
    efficiency = scrapy.Field()

    # 童鞋
    # 适用人群
    people = scrapy.Field()
    # 适用性别
    gender = scrapy.Field()
    # 尺码
    size = scrapy.Field()
    # 风格
    style = scrapy.Field()
    # 评价数
    # comment_count
    # 收藏数
    favcount = scrapy.Field()
    # 地域
    # item_loc

    # chaoshi.tmall
    tmall_sum = scrapy.Field()
    # brandname_list = scrapy.Field()
    pass


class TestItem(scrapy.Item):
    # define the fields for your item here like:
    item_id = scrapy.Field()
    shop_name = scrapy.Field()
    image_urls = scrapy.Field()
    # model = scrapy.Field()
    num = scrapy.Field()
    # item_price = scrapy.Field()
    # sold = scrapy.Field()


class TaobaoItem(scrapy.Item):
    # detail_url = scrapy.Field()
    nid = scrapy.Field()
    raw_title = scrapy.Field()
    sellCount = scrapy.Field()
    img_url = scrapy.Field()
    # brand = scrapy.Field()
    # model = scrapy.Field()
    max_box = scrapy.Field()
    box_size = scrapy.Field()
    box_style = scrapy.Field()






