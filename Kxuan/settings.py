# -*- coding: utf-8 -*-

# Scrapy settings for Kxuan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os
import random
import logging


BOT_NAME = 'Kxuan'

SPIDER_MODULES = ['Kxuan.spiders']
NEWSPIDER_MODULE = 'Kxuan.spiders'

# 多开爬虫
COMMANDS_MODULE = 'Kxuan.mycrawls'

# 小家电商品类别

DEVICE_CATEGORY = ['电压力锅', '电饭煲', '电炖锅', '电饼铛', '养生壶', '电磁炉', '电水壶', '料理机', '豆浆机', '电茶壶', '榨汁机', '电动打蛋机', '酸奶机', '面条机', '咖啡机', '电炖盅', '电蒸锅', '煮蛋器', '绞肉机', '破壁机', '搅拌机', '电热水瓶', '炒锅']
BRANDS = ['Joyoung/九阳', 'SUPOR/苏泊尔', 'Midea/美的', 'Bear/小熊', '九阳', '苏泊尔', '美的', '小熊']

# 大家电，价格抓取
D_APPLIANCES = ['洗衣机', '冰箱']
D_NICKS = ['tcl洗衣机官方旗舰店', '美的官方旗舰店', '三洋官方旗舰店', '海尔官方旗舰店', '小天鹅官方旗舰店', '帝度旗舰店', '惠而浦官方旗舰店', '西门子家电官方旗舰店', '荣事达官方旗舰店', '美的洗衣机旗舰店']
# 洗衣机
D_BRANDS_WASHER = ['TCL', 'Haier/海尔', 'Midea/美的', 'Sanyo/三洋', 'Littleswan/小天鹅', 'SIEMENS/西门子', 'Whirlpool/惠而浦', 'Royalstar/荣事达']
WASHER_MODEL = '''EG10014HBX39GU1,MD100V71WDX,TD100V81WDG,WF100BHIS565S,WD14U5680W,WF100BHIW865W,Radi9S,WF912922BIH0W,EG8014HB39GU1,EG8014HB919SU1,MD80-11WDX,MD80VT715DS5,TD80V80WDG,TD80V160WD,DG-F80570BH,WD14G4681W,XQG80-WD14H4602W,XQG80-WD12G4601W,XQG80-WD14H4682W,XQG80-WD12G4681W,EG10012BKX839SU1,EG10014B39GU1,TG100VT712DS5,Radi10,WF100BS265R,WF100BW865W,WM14U568LW,WM14U7600W,MG90V150WD,MG90-1405WIDQCG,TG90V61WDG,XQG90-P310B,Radi9,Air9s,WF90BW865W,WF90BHIW865W,XQG90-WM12P2689W,WM14U7680W,XQG90-WM12P2601W,XQG90-WM12U5600W,EG8012B919GU1,EG8014B39SU1,MG80V530WD,MG80V330WDX,MG80VT715D5,TG80VT712DG5,WF810320BS0S,WF80BS565S,WG-F80821BW,XQG80-WM10N2C80W,XQG80-WM12P2R88W,XQG80-WM12P2608W,WF80BHS265R,WF80BS265R,WF712921BL5W,WM12L2680W,WM10L2600W,EB80M39TH,MB80-eco11W,TB80-easy60W,WT8655IYM0S,WT8455M0S,EB70Z2WH,MB70V30W,XQB70-S750Z,WT7027M0R,EB55M2WH,MB55V30,WT5455M5S,WT5027M5R,EB80BM2TH,MB80-8100WDQCG,MB80V570WD,TB80-Mute160WD,WT8755BIM0S,sonicV8'''
# 冰箱
D_BRANDS_FRIDGE = ['DIQUA/帝度', 'SIEMENS/西门子', 'Whirlpool/惠而浦']
FRIDGE_MODEL = '''KM46FSG0TI,KA96FS70TI,KA96FA46TI,KA92NS91TI,BCD-516WDBIZW,BCD-592WDBZW,BCD-590WD,BCD-520WDBIZ,BCD-590WDIZ,KA92NE03TI,KA92NV90TI,BCD-610W(KA92NV03TI),KM46FA90TI,BCD-442W(KM48EA30TI),BCD-401W(KM40FA60TI),BCD-401W(KM40FS20TI),BCD-306W(KG32HS26EC),BCD-280W(KG28UA230C),KG28UA240C,KG28US220C,KG28FA291C,BCD-280W(KG28UA290C),KG23D116EW,BCD-321W(KG33NV24EC),KG29NV230C,BCD-268(KG28ES220C)'''

# 生意参谋品牌ID
BS_BRANDS = {
    "Haier/海尔": 11016,
    "Littleswan/小天鹅": 30657,
    "Midea/美的": 30652,
    "SIEMENS/西门子": 80946,
    "Samsung/三星": 81156,
    "Bosch/博世": 3223459,
    "Whirlpool/惠而浦": 66878525,
    "Royalstar/荣事达": 30654,
    "DIQUA/帝度": 50878944,
    "Sanyo/三洋": 10728,
    "TCL": 10858,
    "Panasonic/松下": 81147,
    "Leader/统帅": 113190408,
}

CATEIDS = [
    {'washer': 350301},
    {'fridge': 50003881},
]

WASHER_BRANDS = ['Haier/海尔', 'Littleswan/小天鹅', 'Midea/美的', 'SIEMENS/西门子', 'Sanyo/三洋', 'TCL', 'Panasonic/松下', 'Leader/统帅', 'Royalstar/荣事达', 'Whirlpool/惠而浦']
FRIDGE_BRANDS = ['Haier/海尔', 'SIEMENS/西门子', 'Midea/美的', 'Samsung/三星', 'Bosch/博世', 'Whirlpool/惠而浦', 'Royalstar/荣事达', 'DIQUA/帝度']

# 童鞋子类目
SHOES_SUB = ['公主', '运动', '凉', '拖', '靴']

# 不足条件过滤
NOT_LIST = ['配件', '内胆', '马达', '圈盘', '电源', '风扇', '主板', '显示板', '电阻', '锅盖', '温控器', '盖板', '发热盘', '电热盘', '密封', '胶圈', '电路板', '蒸笼', '开关', '把手', '阀', '键盘', '搅拌杯', '蒸架', '盖子', '接浆', '爸爸', '妈妈', '面板', '旋钮', '过滤网', '研磨', '绞肉杯', '离合', '支架', '刀片', '面盖']


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
MY_USER_AGENT = [
   'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
   'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
   'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
   'Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14C92 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
   'Mozilla/5.0 (iPhone 6; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.6.1 Mobile/13E238 Safari/8536.25',
   'Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
]

MY_USER_AGENT_PC = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
]

'''
CRITICAL - 严重错误(critical)
ERROR - 一般错误(regular errors)
WARNING - 警告信息(warning messages)
INFO - 一般信息(informational messages)
DEBUG - 调试信息(debugging messages)
'''
# 是否启用log日志, 默认开启
# LOG_ENABLED = False
# log编码格式, 默认utf-8
# LOG_ENCODING = ''
# 默认: None，在当前目录里创建logging输出文件的文件名
# 设置日志大小为10m
logging.info('log_file start')
logging.info('kxuan start')
if os.path.exists('./log/kxuan.log') and os.path.getsize('./log/kxuan.log') >= 1024 * 1024 * 2:
   logging.info(os.path.getsize('./log/kxuan.log'))
   os.rename('./log/kxuan.log', './log/kxuan_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
logging.info('washer start')
if os.path.exists('./log/washer.log') and os.path.getsize('./log/washer.log') >= 1024 * 1024 * 2:
   logging.info(os.path.getsize('./log/washer.log'))
   os.rename('./log/washer.log', './log/washer_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
logging.info('fridge start')
if os.path.exists('./log/fridge.log') and os.path.getsize('./log/fridge.log') >= 1024 * 1024 * 2:
   logging.info(os.path.getsize('./log/fridge.log'))
   os.rename('./log/fridge.log', './log/fridge_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))


logging.info('log_file end')
# 默认: 'DEBUG'，log的最低级别, 如果上线后, 最好将级别调成info
LOG_LEVEL = 'INFO'
# 默认: False 如果为 True，进程所有的标准输出(及错误)将会被重定向到log(如果LOG_FILE开启)中。例如，执行 print "hello" ，其将会在Scrapy log中显示
# LOG_STDOUT = True


# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
   # 'User-Agent': random.choice(MY_USER_AGENT),
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
# }



IMAGES_STORE = 'images'

# 多个爬虫自定义多个setting
custom_settings_for_tmall = {
    'DOWNLOAD_DELAY': 1,
    'LOG_FILE': './log/kxuan.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Kxuan.pipelines.TmallPipeline': 300,
        'Kxuan.pipelines.PicImagePipeline': 1,
    },
    'DEFAULT_REQUEST_HEADERS': {
       # 'User-Agent': random.choice(MY_USER_AGENT),
      # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      # 'Accept-Language': 'en',
       'Cookie': 'sm4=330100; cna=p06hE64hcF0CAXARX/O1H59e; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; lid=%E8%8D%A3%E4%BA%8B%E8%BE%BE%E7%94%B5%E5%99%A8%E6%97%97%E8%88%B0%E5%BA%97; _uab_collina=153144438823019145360567; t=353065b89f6de4884ac4996fe6b330f1; _tb_token_=55835ee9be7e7; cookie2=1c4c479630cfb270aefeb824b9912db2; ck1=""; _umdata=0712F33290AB8A6D28818509BA73E9E5CC6C608B1827CC9B9220DBC0737F67C037C5CDB93F92CAD0CD43AD3E795C914C400FF0F360DABD8F402E8A3A972C5B37; pnm_cku822=098%23E1hvLvvUvbpvUvCkvvvvvjiPPsz9gjtVPssvljthPmP9AjlRPF5ZAjrWRLdZ1jtWiQhvCvvvpZpEvpCWvmyNj10xdXkOd56OfakKDf8rwZXl%2Bb8reE%2BaUWFZe3RAdcHvafmAdXkwjo2tD40OeTt%2Bm7zheTTJVcxveE7reEkKfvDr1EkK5FGDNIyCvvOCvhEC0nAivpvUvvCCE4g8zYRtvpvIvvCvxQvvvpZvvhxmvvmCPQvvBGwvvvUwvvCj1Qvv9JGvvhxmvvmCqQhCvvOv9hCvvvvPvpvhvv2MMsyCvvpvvhCv; res=scroll%3A1287*5756-client%3A1287*894-offset%3A1287*5756-screen%3A1920*1080; cq=ccp%3D1; _m_h5_tk=f8dc288a9f1cfb22ac014d62bdd81328_1531897009134; _m_h5_tk_enc=630dfb70b00c0a61a8b352929400c1c6; x5sec=7b22746d616c6c7365617263683b32223a2234613534316566636231646634613538613030656237653434383930326431374349484175396f46454c43446e7372582f71367251673d3d227d; uc1=cookie14=UoTfKjykOkMMlw%3D%3D&lng=zh_CN; uc3=id2=&nk2=&lg2=; tracknick=""; lgc=""; csg=78a1e9b1; skt=6a2b3725d7fe5259; hng=CN%7Czh-CN%7CCNY%7C156; sn=%E7%BE%8E%E7%9A%84%E7%82%8A%E5%85%B7%E6%97%97%E8%88%B0%E5%BA%97%3A%E5%8A%A9%E7%90%86; enc=2HD9%2B4bRR8Th%2FQS7PnLsNXbhUHthF5fLN3w1gd6HqpMNd914853QmcW0xANcAVAKdFcUGpvw5bV2dmVxiQXHtg%3D%3D; tt=chaoshi.tmall.com; isg=BBUVTVlN4hrjzsa11SgtJLRiJBdjDapHNgO6u5e6WQzb7jXgX2LZ9CPvvLJ9buHc',
    },
}

custom_settings_for_washer = {
    'DOWNLOAD_DELAY': 5,
    'LOG_FILE': './log/washer.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Kxuan.pipelines.WasherPipeline': 400,
    },
}

custom_settings_for_fridge = {
    'DOWNLOAD_DELAY': 5,
    'LOG_FILE': './log/fridge.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Kxuan.pipelines.FridgePipeline': 500,
    },
}

custom_settings_for_taobao = {
    'DOWNLOAD_DELAY': 1,
    'LOG_FILE': './log/taobao.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'DEFAULT_REQUEST_HEADERS': {
        'User-Agent': random.choice(MY_USER_AGENT_PC),
        'Cookie': 't=353065b89f6de4884ac4996fe6b330f1; cookie2=1acfc7209af056a07486f75b191ed584; _tb_token_=55ee6e9335be5; cna=p06hE64hcF0CAXARX/O1H59e; mt=ci=0_0; x=761383686; uc1=cookie14=UoTeNmdb74zh6g%3D%3D&lng=zh_CN; uc3=nk2=&id2=&lg2=; tracknick=; sn=%E4%B8%89%E6%B4%8B%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%95%B0%E6%8D%AE%E7%BB%84; csg=30b3d3ee; unb=3789122802; skt=c17d6912a18e6687; v=0; thw=cn; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; hng=CN%7Czh-CN%7CCNY%7C156; enc=sCk%2Bjb89sAF0bqEQO%2Fy7JdHeVZe2PnWR2TtrgmupFi1GW1KOuzh7kpb8I5QDJcPIXg5f1iVZWPqJ5ziGZUmOMQ%3D%3D; _m_h5_tk=3d121e1fc45e8ff4a6a775b12c0b726c_1528696756676; _m_h5_tk_enc=2de2fe2c2d4f70347aab6ff8180f7243; JSESSIONID=3B2EA7EB61B7575B724D21872F1259B7; isg=BH9_B5DkGKj4pRy3yV-7xRXvDlWle7FdnZYOhxFNci-tIJyiGTSsV1L2ZvDeeKt-',
    },
    'ITEM_PIPELINES': {
        'Kxuan.pipelines.TaobaoPipeline': 500,
    },
}


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Kxuan.middlewares.KxuanSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Kxuan.middlewares.KxuanDownloaderMiddleware': 543,
   # 'Kxuan.middlewares.MyUserAgentMiddleware': 543,
   'Kxuan.middlewares.ProxyMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
   # 'Kxuan.pipelines.KxuanPipeline': 301,
   # 'Kxuan.pipelines.CsvPipeline': 300,
   # 'Kxuan.pipelines.RicePipeline': 100,
   # 'Kxuan.pipelines.TmallPipeline': 300,
   # 'Kxuan.pipelines.WasherPipeline': 400,
   # 'Kxuan.pipelines.FridgePipeline': 500,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
