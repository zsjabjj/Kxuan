# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
import io
import json
import logging
import os
import csv
import shutil
import time
from urllib import request

import scrapy
import xlsxwriter
import xlwt
from PIL import Image
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from Kxuan.checkpipeline import check_spider_pipeline
from Kxuan.format_style import xlsx_style
from Kxuan.settings import WASHER_MODEL, FRIDGE_MODEL, BRANDS
from tu_pinjie import add_num, tu_pj


class TmallPipeline(object):
    '''猫超竞品价格'''
    # 表头字段名
    tmall_colname = [
        'device_category',
        'brand',
        'model',
        'item_price',
        'hand_price',
        'month_sold_detail',
        'month_sold_list',
        'week_sold',
        'item_title',
        'detail_url',
        'pic_url',
        'item_nid',
        'reserve_price',
        'post_fee',
        # 'brandname_list',
    ]
    # 表头字段名
    colname = [
        'device_category',
        'brand',
        'model',
        'item_price',
        'hand_price',
        'month_sold_detail',
        'month_sold_list',
        # 'week_sold',
        'item_title',
        'detail_url',
        'pic_url',
        'item_nid',
        'tmall_sum',
    ]

    # 初始化
    def open_spider(self, spider):
        '''初始化'''
        # 建立存储文件夹
        self.folder = './tmall/tmall_%s/' % (datetime.datetime.now().strftime("%Y%m%d"))
        # 判断文件夹是否存在
        if os.path.exists(self.folder):
            logging.info('exists')
        else:
            os.mkdir(self.folder)

        # 建立存储文件名
        filename = self.folder + '%s_%s.csv' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        filename_liven = self.folder + '%s_liven_%s.csv' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        # 判断文件是否存在
        if os.path.exists(filename):
            logging.info('remove csv start')
            os.remove(filename)
            logging.info('remove csv end')

        logging.info('create csv')
        # 在爬虫启动时，创建csv，编码已经修改
        self.file = codecs.open(filename, 'a', 'utf_8_sig')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.tmall_colname)
        # 写入字段名称作为首行
        self.writer.writeheader()

        # 添加利仁
        self.file_liven = codecs.open(filename_liven, 'a', 'utf_8_sig')
        # 启动csv的字典写入方法
        self.writer_liven = csv.DictWriter(self.file_liven, self.tmall_colname)
        # 写入字段名称作为首行
        self.writer_liven.writeheader()



        # 创建excel工作表
        self.workbook = xlwt.Workbook(encoding='utf-8')
        # Exception: Attempt to overwrite cell: sheetname='sheet1' rowx=1 colx=0 如下处理
        self.worksheet = self.workbook.add_sheet('sheet1', cell_overwrite_ok=True)

        # 设置表头
        num = 0
        for col in self.colname:
            self.worksheet.write(0, num, label=col)
            num += 1
        self.val1 = 1

    @check_spider_pipeline
    def process_item(self, item, spider):
        '''数据开始存储'''
        # logging.info('save csv')
        if 'image_urls' in item:

            return item

        try:
            if item['brand'] in BRANDS:
                # logging.info(item['brand'])
                if '炒锅' == item['device_category']:
                    if 'CL32T1' in item['item_title'] or 'MP-WCT30A02' in item['item_title']:
                        self.writer.writerow(item)
                else:
                    self.writer.writerow(item)
                    self.writer_liven.writerow(item)

            # 添加利仁
            elif '利仁' in item['item_title'] and 'LR-280A' in item['item_title']:
                self.writer_liven.writerow(item)
        except Exception as err:
            logging.info(err)
            

        # 将json字典写入excel
        # 变量用来循环时控制写入单元格，感觉有更好的表达方式
        try:
            hand_price = int(item['hand_price'])
        except:
            if '满' in item['hand_price']:
                hand_price = int(''.join(item['item_price'].split('.'))) / 100
            else:
                hand_price = int(''.join(item['hand_price'].split('.'))) / 100
        try:
            item['tmall_sum'] = hand_price * int(item['month_sold_detail'])
        except:
            item['tmall_sum'] = str(hand_price) + '*' + item['month_sold_detail']
        # for list_item in data:
        for key, value in item.items():
            for index, col in enumerate(self.colname):
                if key == col:
                    self.worksheet.write(self.val1, index, value)

                else:
                    pass
        self.val1 += 1
        self.worksheet.write(len(self.colname), len(self.colname) - 1, item['tmall_sum'])
        logging.info('write xls file success!')
        # return item


    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        spider.logger.info('%s finished' % spider.name)
        # self.f.close()
        self.file.close()
        self.file_liven.close()
        # 保存
        file_name = './tmall/' + 'tamllAll_%s.xls' % datetime.datetime.now().strftime('%Y%m')

        if os.path.exists(file_name):
            pass
        else:
            self.workbook.save(file_name)


class PicImagePipeline(ImagesPipeline):
    '''图片处理'''
    def __init__(self, store_uri, download_func=None, settings=None):
        super(PicImagePipeline, self).__init__(store_uri, settings=settings, download_func=download_func)
        try:
            shutil.rmtree('/Users/tiger007/Desktop/shell_test/Kxuan/images')
        except Exception as err:
            shutil.move('images', 'images_%s' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            logging.error(err)

        self.folder = './tmall/pic_%s/' % (datetime.datetime.now().strftime("%Y%m%d"))

        if os.path.exists(self.folder):
            logging.info('exists')
        else:
            os.mkdir(self.folder)

        self.filename = '%s_%s.xlsx' % ('tmallpic', datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        # self.filename_more = '%s_%s.xlsx' % ('moreBrand', datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    def get_media_requests(self, item, info):

        # print(item)
        # for image_url in item['image_urls']:
        if 'image_urls' not in item:
            return item
        try:
            image_url = item['image_urls']
            yield scrapy.Request(image_url)
        except Exception as err:
            logging.error(err)
            # logging.info('image pipeline:')
            return item

    def item_completed(self, results, item, info):
        '''图片处理'''
        try:
            text = '''
                %s
                页面价: %s
                月销量: %s
            ''' % (item['shop_name'], item['item_price'], item['month_sold_list'])
        except Exception as err:
            logging.error(err)
            return item

        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:
            raise DropItem("Item contains no images")
        if item['model']:
            newname = item['model'] + '_%s.jpg' % item['num']
        else:
            newname = item['shop_name'] + '-' + item['model'] + '.jpg'

        try:
            os.rename("./images/" + image_paths[0], "./images/full/" + newname)
            time.sleep(1)
            image = Image.open('./images/full/%s' % newname).convert('RGB')
            add_num(image, newname, text)
        except Exception as err:
            logging.error(err)

        return item

    def __del__(self):


        line_list = [line.strip() for line in open('./model.txt') if line]

        filename_list = os.listdir('./images/fullNew')

        logging.info('start xlsx')

        # 创建一个新的excel文件并添加一个工作表
        wb = xlsxwriter.Workbook(self.folder + self.filename)
        ws = wb.add_worksheet(self.filename)

        # worksheet.set_row(0,40,cell_format)    设置第一行高40,加粗
        # worksheet.set_column('A:A',20) #设置第一列宽度为20像素

        cell_format = wb.add_format({'align': 'center', 'valign': 'vcenter'})

        # 行，列初始值
        row = 0
        col = 0

        # 设置表头
        for coln in ['型号', '图片1', '图片2', '图片3', '图片4', '图片5']:
            ws.write(row, col, coln)
            col += 1

        for line1 in line_list:

            row += 1
            ws.set_row(row, height=20)

            for i in range(1, 6):
                img_name = line1 + '_' + str(i) + '.jpg'
                try:
                    use_name = filename_list.pop(filename_list.index(img_name))
                except:
                    logging.error(img_name)
                else:
                    img_path = './images/fullNew/' + use_name

                    ws.insert_image(
                        # 'B2',
                        row,
                        i,
                        img_path,
                        {
                            # 'url': 'https://img.alicdn.com/imgextra/i4/859230932/TB18FhcmVmWBuNjSspdXXbugXXa_!!0-item_pic.jpg',
                            'x_scale': 0.025,
                            'y_scale': 0.025,
                        }
                    )
                finally:
                    ws.write(row, 0, line1)
                    ws.set_column(0, 0, width=16, cell_format=cell_format)


        # 表格存储结束
        wb.close()

        logging.info('end xlsx')



class WasherPipeline(object):
    '''洗衣机竞品价格'''
    w_colname = [
        'device_category',
        'item_nid',
        'category',
        'capacity',
        'model',
        'brand',
        'nick',
        'item_title',
        'detail_url',
        'pic_url',
        'item_price',
        'hand_price',
        'activity',
        'offer',
        'month_sold_list',
        'month_sold_detail',
    ]

    colname = [
        'date_time',
        'category',
        'capacity',
        'model',
        'brand',
        'nick',
        'item_title',
        'detail_url',
        'pic_url',
        'item_price',
        'hand_price',
        'activity',
        'offer',
        'mini_pic'
    ]

    def open_spider(self, spider):
        folder = './tmall/tmall_%s/' % datetime.datetime.now().strftime("%Y%m%d")
        if os.path.exists(folder):
            print('exists')
        else:
            os.mkdir(folder)

        print('start write %s' % spider.name)
        filename = folder + '%s_%s.csv' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        if os.path.exists(filename):
            print('remove csv start')
            os.remove(filename)
            print('remove csv end')
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        print('create csv')
        self.file = open(filename, 'a', newline='')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.w_colname)

        # 写入字段名称作为首行
        self.writer.writeheader()

        # 创建一个新的excel文件并添加一个工作表
        self.wb = xlsxwriter.Workbook(folder + '%s_%s.xlsx' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        self.ws = self.wb.add_worksheet()

        # 行，列初始值
        self.row = 0
        self.col = 0

        # 设置表头
        for coln in self.colname:
            self.ws.write(self.row, self.col, coln)
            self.col += 1

        # # 创建excel工作表
        # self.workbook = xlwt.Workbook(encoding='utf-8')
        # # Exception: Attempt to overwrite cell: sheetname='sheet1' rowx=1 colx=0 如下处理
        # self.worksheet = self.workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        #
        # # 设置表头
        # num = 0
        # for col in self.colname:
        #     self.worksheet.write(0, num, label=col)
        #     num += 1
        #     # self.worksheet.write(0, 1, label='LEN')
        #     # self.worksheet.write(0, 2, label='ID')
        #     # self.worksheet.write(0, 3, label='OTHER')
        # self.val1 = 1
        # # self.val2 = 1
        # # self.val3 = 1
        # # self.val4 = 1

    @check_spider_pipeline
    def process_item(self, item, spider):

        print('save csv')
        print(type(item))
        if item['model'] in WASHER_MODEL:
            # 时间字段
            date_time = datetime.datetime.now().strftime('%Y%m%d')
            # 行的移动
            self.row += 1
            # 写入时间数据
            self.ws.write(self.row, 0, date_time)
            # 写入主要数据
            for key, value in item.items():
                for index, col in enumerate(self.colname):
                    if key == col:
                        self.ws.write(self.row, index, value)

            # 存图片
            image_data = io.BytesIO(request.urlopen(item['pic_url']).read())
            self.ws.insert_image(
                # 'B113',
                self.row,
                len(self.colname) - 1,
                item['pic_url'],
                {
                    'image_data': image_data,
                    'x_scale': 0.025,
                    'y_scale': 0.025,
                }
            )
        # json.dumps(item, ensure_ascii=False).encode()
        # 把每次输出的item，写入csv中
        self.writer.writerow(item)
        return item
        # # 将json字典写入excel
        # # 变量用来循环时控制写入单元格，感觉有更好的表达方式
        #
        # # for list_item in data:
        # for key, value in item.items():
        #     for index, col in enumerate(self.colname):
        #         if key == col:
        #             self.worksheet.write(self.val1, index, value)
        #
        #         else:
        #             pass
        # self.worksheet.write(self.val1, 0, datetime.datetime.now().strftime("%Y%m%d"))
        # self.worksheet.write(self.val1, 0, datetime.datetime.now().strftime("%Y%m%d"))
        #
        # self.val1 += 1
        # self.worksheet.write(len(self.colname), len(self.colname) - 1, item['tmall_sum'])

    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        spider.logger.info('%s finished' % spider.name)
        self.file.close()

        # 表格存储结束
        self.wb.close()

        # 保存数据后对表格进一步处理



class FridgePipeline(object):
    '''冰箱竞品价格'''
    w_colname = [
        'device_category',
        'item_nid',
        'category',
        'capacity',
        'model',
        'brand',
        'nick',
        'item_title',
        'detail_url',
        'pic_url',
        'item_price',
        'hand_price',
        'activity',
        'offer',
        'month_sold_list',
        'month_sold_detail',
        'fridge_method',
        'efficiency',
    ]

    colname = [
        'date_time',
        'category',
        'capacity',
        'model',
        'brand',
        'nick',
        'item_title',
        'detail_url',
        'pic_url',
        'item_price',
        'hand_price',
        'activity',
        'offer',
        'fridge_method',
        'efficiency',
        'mini_pic'
    ]

    def open_spider(self, spider):
        folder = './tmall/tmall_%s/' % (datetime.datetime.now().strftime("%Y%m%d"))
        if os.path.exists(folder):
            print('exists')
        else:
            os.mkdir(folder)

        print('start write %s' % spider.name)
        filename = folder + '%s_%s.csv' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        if os.path.exists(filename):
            print('remove csv start')
            os.remove(filename)
            print('remove csv end')
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        print('create csv')
        self.file = open(filename, 'a', newline='')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.w_colname)

        # 写入字段名称作为首行
        self.writer.writeheader()

        # 创建一个新的excel文件并添加一个工作表
        self.wb = xlsxwriter.Workbook(
            folder + '%s_%s.xlsx' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        self.ws = self.wb.add_worksheet()
        # # 列宽
        # self.ws.set_column()
        # # 行高
        # self.ws.set_row()

        # 行，列初始值
        self.row = 0
        self.col = 0

        # 设置表头
        for coln in self.colname:
            self.ws.write(self.row, self.col, coln)
            self.col += 1

    @check_spider_pipeline
    def process_item(self, item, spider):
        print('save csv')
        print(type(item))
        if item['model'] in FRIDGE_MODEL:
            # 时间字段
            date_time = datetime.datetime.now().strftime('%Y%m%d')
            # 行的移动
            self.row += 1
            # 写入时间数据
            self.ws.write(self.row, 0, date_time)
            # 写入主要数据
            for key, value in item.items():
                for index, col in enumerate(self.colname):
                    if key == col:
                        self.ws.write(self.row, index, value)

            # 存图片
            image_data = io.BytesIO(request.urlopen(item['pic_url']).read())
            self.ws.insert_image(
                # 'B113',
                self.row,
                len(self.colname) - 1,
                item['pic_url'],
                {
                    'image_data': image_data,
                    'x_scale': 0.025,
                    'y_scale': 0.025,
                }
            )
        # json.dumps(item, ensure_ascii=False).encode()
        # 把每次输出的item，写入csv中
        self.writer.writerow(item)
        # if item['model'] in FRIDGE_MODEL:
        #     # json.dumps(item, ensure_ascii=False).encode()
        #     # 把每次输出的item，写入csv中
        #     self.writer.writerow(item)
        #     # return item
        return item

    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        spider.logger.info('%s finished' % spider.name)
        self.file.close()

        # 表格存储结束
        self.wb.close()


class GshoesPipeline(object):
    '''鞋子竞品价格'''
    w_colname = [
        'item_nid',
        'device_category',
        'brand',
        'nick',
        'item_price',
        'month_sold_detail',
        'month_sold_list',
        'item_title',
        'people',
        'gender',
        'size',
        'style',
        'comment_count',
        'favcount',
        'item_loc',
        'detail_url',
        'pic_url',
    ]

    def open_spider(self, spider):
        folder = './tmall/tmall_%s/' % (datetime.datetime.now().strftime("%Y%m%d"))
        if os.path.exists(folder):
            print('exists')
        else:
            os.mkdir(folder)

        print('start write %s' % spider.name)
        filename = folder + '%s_%s.csv' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        if os.path.exists(filename):
            print('remove csv start')
            os.remove(filename)
            print('remove csv end')
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        print('create csv')
        self.file = open(filename, 'a', newline='')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.w_colname)

        # 写入字段名称作为首行
        self.writer.writeheader()

    @check_spider_pipeline
    def process_item(self, item, spider):
        print('save csv')
        print(type(item))
        # json.dumps(item, ensure_ascii=False).encode()
        # 把每次输出的item，写入csv中
        self.writer.writerow(item)
        # return item

    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        spider.logger.info('%s finished' % spider.name)
        self.file.close()


class TaobaoPipeline(object):
    colname = [
        '品牌',
        '型号',
        '类型',
        '容量段',
        '月销',
        '图片',
        '链接',
    ]

    def open_spider(self, spider):
        # self.folder = './tmall/top100_%s/' % datetime.datetime.now().strftime("%Y%m%d")
        #
        # if os.path.exists(self.folder):
        #     print('exists')
        # else:
        #     os.mkdir(self.folder)

        self.filename = './%s_%s.xlsx' % (spider.name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

        # 创建一个新的excel文件并添加一个工作表
        self.wb = xlsxwriter.Workbook(self.filename)
        # 创建工作簿
        self.ws = self.wb.add_worksheet('嵌入式冰箱统计')
        # print('chuang jian trend')

        self.center_style = self.wb.add_format(xlsx_style())

        # 行，列初始值
        self.row = 0
        self.col = 0

        # 设置表头
        for coln in self.colname:
            self.ws.write(self.row, self.col, coln, self.center_style)
            self.col += 1

    def process_item(self, item, spider):

        self.row += 1

        item_dict = dict()



        item_dict['品牌'] = item['brand']
        try:
            item_dict['型号'] = item['model']
        except:
            item_dict['型号'] = ''

        item_dict['类型'] = item['box_style']
        try:
            item_dict['容量段'] = item['max_box']
        except:
            item_dict['容量段'] = ''
        item_dict['月销'] = item['sellCount']
        # item_dict['图片'] = item['paySubOrderCnt']
        item_dict['链接'] = item['detail_url']

        print('write data:', item_dict)
        print('start write data')
        for item_num in range(0, len(self.colname)):
            if '图片' == self.colname[item_num]:
                url = item['img_url']
                if url.endswith('gif'):
                    logging.error(url)
                else:
                    image_data = io.BytesIO(request.urlopen(url).read())
                    self.ws.insert_image(
                        self.row,
                        item_num,
                        url,
                        {
                            'image_data': image_data,
                            'x_scale': 0.025,
                            'y_scale': 0.025,
                        }
                    )
                    pass
            else:

                self.ws.write(self.row, item_num, item_dict[self.colname[item_num]], self.center_style)
            self.ws.set_row(self.row, 25)  # 设置行高25
        print('end write data')
        print('+' * 30)


    def close_spider(self, spider):
        self.wb.close()

