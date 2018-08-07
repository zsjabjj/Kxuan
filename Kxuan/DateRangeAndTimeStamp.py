import datetime
import re
import time
import logging

'''
t = time.strptime('2018-04-28', '%Y-%m-%d')
int(time.mktime(t))
'''
# class DaterangeAndTimestamp(object):


    # def judge_date(self, date):


def date_range():
    print('''
    例如：今天是2018年04月28日，想看昨天的数据，startdate输入2018-04-27
    enddate输入2018-04-27，若想看近期一周的数据，startdate输入2018-04-21
    enddate输入2018-04-27，若自定义输入也可以，只要符合输入要求 
    ''')

    while True:
        while True:
            startdate = input('请输入起始日期(格式例如 2018-01-01):')
            if len(startdate) != 10:
                logging.error('格式输入有误，请重新输入！')
                continue
            elif '-' not in startdate:
                logging.error('格式输入有误，请重新输入！')
                continue
            elif len(startdate.split('-')) != 3:
                logging.error('格式输入有误，请重新输入！')
                continue
            else:
                cur = datetime.datetime.now()
                try:
                    Year, Month, Day = re.findall(r'(\d+)-(\d+)-(\d+)', startdate)[0]
                except Exception as e:
                    logging.error('您输入的日期超出范围或日期有问题，请重新输入！')
                    continue
                try:
                    Year = int(Year)
                    Month = int(Month)
                    Day = int(Day)
                except:
                    logging.error('格式输入有误，请重新输入！')
                    continue
                if Year > cur.year:
                    logging.error('输入日期年份超出范围，请重新输入！')
                    continue
                elif Month > cur.month or Day > cur.day:
                    logging.error('输入日期超出范围，请重新输入！')
                    continue
                logging.info(Year, Month, Day)
                break


        while True:
            enddate = input('请输入截止日期(格式例如 2018-01-01):')
            if len(enddate) != 10:
                logging.error('格式输入有误，请重新输入！')
                continue
            elif '-' not in enddate:
                logging.error('格式输入有误，请重新输入！')
                continue
            elif len(enddate.split('-')) != 3:
                logging.error('格式输入有误，请重新输入！')
                continue
            else:
                cur = datetime.datetime.now()
                try:
                    Year, Month, Day = re.findall(r'(\d+)-(\d+)-(\d+)', enddate)[0]
                except Exception as e:
                    logging.error('您输入的日期超出范围或日期有问题，请重新输入！')
                    continue
                try:
                    Year = int(Year)
                    Month = int(Month)
                    Day = int(Day)
                except:
                    logging.error('格式输入有误，请重新输入！')
                    continue
                if Year > cur.year:
                    logging.error('输入日期年份超出范围，请重新输入！')
                    continue
                elif Month > cur.month or Day > cur.day:
                    logging.error('输入日期超出范围，请重新输入！')
                    continue
                logging.info(Year, Month, Day)
                break

        start_date = time.strptime(startdate, '%Y-%m-%d')
        start = int(time.mktime(start_date))
        end_date = time.strptime(enddate, '%Y-%m-%d')
        end = int(time.mktime(end_date))

        if start > end:
            logging.error('日期选取出错，请重新选取！')
            continue
        else:
            break


    return startdate, enddate



def time_stamp():
    return ''.join(str(time.time()).split('.'))[:13]


if __name__ == '__main__':
    # d = DaterangeAndTimestamp()
    print(time_stamp())
    print(date_range())
