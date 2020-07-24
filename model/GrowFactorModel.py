#-*- coding:utf-8 -*-

GUANG_FACTOR = 'guang'
WEN_DU_FACTOR = 'wendu'
SHI_DU_FACTOR = 'shidu'
EC_FACTOR = 'ec'
CO2_FACTOR = 'co2'
SOIL_WEN_DU_FACTOR = 'soilwendu'
SOIL_SHI_DU_FACTOR = 'soilshidu'


GUANG_FACTOR_CODE = 103;
WEN_DU_FACTOR_CODE = 101;
SHI_DU_FACTOR_CODE = 102;
EC_FACTOR_CODE = 202;
CO2_FACTOR_CODE = 104;
SOIL_WEN_DU_FACTOR_CODE = 204;
SOIL_SHI_DU_FACTOR_CODE = 201;


GUANG_FACTOR_NAME = '光照'
WEN_DU_FACTOR_NAME = '空气温度'
SHI_DU_FACTOR_NAME = '空气湿度'
EC_FACTOR_NAME = 'EC值'
CO2_FACTOR_NAME = 'CO2'
SOIL_WEN_DU_FACTOR_NAME = '土壤温度'
SOIL_SHI_DU_FACTOR_NAME = '土壤含水量'


#影响植物成长因素。白天和晚上的最优值不一样
DAY_CODE = 1;
NIGHT_CODE = 2;

#影响植物成长的因素
class GrowFactor:

    #成长要素受到在白天，晚上，以及不同的生长阶段，值不一定相同，一天中不同的时间点，最优值不一定相同
    #初始化时，影响植物成长的因素默认没有值
    def __init__(self):
        self.guang = '';
        self.wendu = '';
        self.shidu = '';
        self.ec = '';
        self.co2 = '';
        self.soilwendu = '';
        self.soilshidu = '';
        self.grow_state = '';
        self.grow_state_code = 0;
        self.day_time = ''#时间，对应白天或晚上
        self.now_hour = ''#默认没有时间


