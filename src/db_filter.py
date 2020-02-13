
import pymysql
import time
from src.config import WEIBO_SPIDER_CONFIG

THE_RESPON_DATA_CODE = (
    'ok',
    'unkonwn error',
    'the database is wrong',
    'the result of your query is null',
    'your params are error'
)

class DbFilter:
    key = ('id', 'time', 'pos', 'desc', "desc_extr")

    def __init__(self, args=None):
        self.args = args
        self.db = pymysql.connect(
            host=WEIBO_SPIDER_CONFIG['database']['host'],
            port=WEIBO_SPIDER_CONFIG['database']['port'],
            user=WEIBO_SPIDER_CONFIG['database']['user'],
            password=WEIBO_SPIDER_CONFIG['database']['password'],
            database=WEIBO_SPIDER_CONFIG['database']['name'],
        )
        self.cursor = self.db.cursor()
        self.data = {'code':1,'data':[], 'msg':THE_RESPON_DATA_CODE[1]}


    def __del__(self):
        self.db.close()


    def set_args(self, args):
        self.args = args


    def set_error(self, code):
        self.data['code'] = code
        self.data['data'] = []
        self.data['msg'] = THE_RESPON_DATA_CODE[code]
        return self.data


    def get_data_from_db(self, sql):
        try:
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()
        except:
            self.set_error(2)
        else:
            if not self.result:
                self.set_error(3)
            else:
                for i, t in enumerate(self.result):
                    t = list(t)         # 元组转换为数组
                    t[1] = str(t[1])    # datetime类型数据转换为字符串
                    self.data['data'].append(dict(zip(self.key, t)))
                self.data['code'] = 0
                self.data['msg'] = THE_RESPON_DATA_CODE[0]
        return self.data


    def get_data_by_time(self):
        if 'from' not in self.args and 'to' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_realtime`"
        elif 'to' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE `time` >= from_unixtime({0},'%Y-%m-%d %H:%i:%s')".format(self.args['from'])
        elif 'from' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE `time` <= from_unixtime({0},'%Y-%m-%d %H:%i:%s')".format(self.args['to'])
        else:
            if self.args['from'] > self.args['to']:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`time` >= from_unixtime({0},'%Y-%m-%d %H:%i:%s') AND \
                    `time` <= from_unixtime({1},'%Y-%m-%d %H:%i:%s'))".format(self.args['to'], self.args['from'])
            else:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`time` >= from_unixtime({0},'%Y-%m-%d %H:%i:%s') AND \
                    `time` <= from_unixtime({1},'%Y-%m-%d %H:%i:%s'))".format(self.args['from'], self.args['to'])
        return self.get_data_from_db(sql)


    def get_data_by_pos(self):        
        if 'from' not in self.args and 'to' not in self.args:
            return self.set_error(4)
        elif 'to' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`pos` = {0})".format(self.args['from'])
        elif 'from' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`pos` = {0})".format(self.args['to'])
        else:            
            if self.args['from'] > self.args['to']:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`pos` >= {0} AND `pos` <= {1})".format(self.args['to'], self.args['from'])
            else:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`pos` >= {0} AND `pos` <= {1})".format(self.args['from'], self.args['to'])
        return self.get_data_from_db(sql)


    def get_data_by_desc(self):
        try:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE `desc` = '{0}'".format(self.args['name'])
        except KeyError:
            return self.set_error(4)
        else:
            return self.get_data_from_db(sql)


    def get_data_by_desc_extr(self):
        if 'from' not in self.args and 'to' not in self.args:
            return self.set_error(4)
        elif 'to' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`desc_extr` > {0})".format(self.args['from'])
        elif 'from' not in self.args:
            sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`desc_extr` < {0})".format(self.args['to'])
        else:
            if self.args['from'] > self.args['to']:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`desc_extr` >= {0} AND `desc_extr` <= {1})".format(self.args['to'], self.args['from'])
            else:
                sql = "SELECT * FROM  `weibo_topdata_all` WHERE (`desc_extr` >= {0} AND `desc_extr` <= {1})".format(self.args['from'], self.args['to'])
        return self.get_data_from_db(sql)


    def get_data(self):
        if self.args['by'] == '1':
            return self.get_data_by_time()
        elif self.args['by'] == '2':
            return self.get_data_by_pos()
        elif self.args['by'] == '3':
            return self.get_data_by_desc()
        elif self.args['by'] == '4':
            return self.get_data_by_desc_extr()
        else:
            return self.set_error(4)
