import random
import logging

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from Kxuan.settings import MY_USER_AGENT_PC


def singleton(D):
    class C(D):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = D.__new__(cls, *args, **kwargs)
            return cls._instance

    C.__name__ = D.__name__

    return C


@singleton
class Fire(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent=%s' % random.choice(MY_USER_AGENT_PC))
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        self.driver.implicitly_wait(3)

    def getdriver(self):
        return self.driver

    def __del__(self):
        self.driver.quit()

    def get_sell(self, data):
        url = 'https://detail.tmall.com/item.htm?id={id}'.format(id=data['item_nid'])
        self.driver.get(url)
        try:
            # 模拟浏览器页面抓取月销量
            logging.info(data['item_title'], self.driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text)
            sell_count = self.driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
            # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]
        except:
            sell_count = data['month_sold_list']
        # time.sleep(0.5)
        # driver.quit()

        return sell_count


def request_detail(data):
    '''
    网页上获取月销量
    :param data: 包含itemID和item_title的字典
    :return : sell_count月销量
    '''
    url = 'https://detail.tmall.com/item.htm?id={id}'.format(id=data['item_nid'])
    # # phantomjs设置请求头
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (random.choice(MY_USER_AGENT_PC))
    # driver = webdriver.PhantomJS(
    #     executable_path='/usr/local/bin/phantomjs',
    #     desired_capabilities=dcap)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=%s' % random.choice(MY_USER_AGENT_PC))
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
    # driver.get("https://cnblogs.com/")

    # # Chrome设置请求头
    # # 进入浏览器设置
    # options = webdriver.ChromeOptions()
    # # 设置中文
    # options.add_argument('lang=zh_CN.UTF-8')
    # # 更换头部
    # options.add_argument(
    #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    # browser = webdriver.Chrome(chrome_options=options)

    # driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS()

    driver.implicitly_wait(3)
    driver.get(url)
    try:
        # 模拟浏览器页面抓取月销量
        print(data['item_title'],
              driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text)
        sell_count = driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
        # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]
    except:
        sell_count = data['month_sold_list']
    # time.sleep(0.5)
    driver.quit()

    return sell_count


if __name__ == '__main__':
    data = {'item_nid': 557756812794, 'item_title': 'KM46FSG0TI', 'month_sold_list': 35}
    sell_count = request_detail(data)
    print(sell_count)
