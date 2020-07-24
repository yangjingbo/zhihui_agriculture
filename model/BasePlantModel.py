#-*- coding:utf-8 -*-

NO_GROW_STATE_CODE = 0;
NO_GROW_STATE = '无'#暂时没有GROW_STATE的数据
DEFAULT_TOTAL_GROW_STATE = 6 #成长模型里面默认值为6，表示有6个成长阶段

#一天的时间
ZERO_HOUR = "00:00-01:00";
FIRST_HOUR = "01:00-02:00";
SECOND_HOUR = "02:00-03:00";
THIRD_HOUR = "03:00-04:00";
FOURTH_HOUR = "04:00-05:00";
FIVE_HOUR = "05:00-06:00";
SIX_HOUR = "06:00-07:00";
SEVEN_HOUR = "07:00-08:00";
EIGHT_HOUR = "08:00-09:00";
NINE_HOUR = "09:00-10:00";
TEN_HOUR = "10:00-11:00";
ELEVEN_HOUR = "11:00-12:00";
TWELVE_HOUR = "12:00-13:00";
THIRTEEN_HOUR = "13:00-14:00";
FOURTHEEN_HOUR = "14:00-15:00";
FIFTEEN_HOUR = "15:00-16:00";
SIXTEEN_HOUR = "16:00-17:00";
SEVENTEEN_HOUR = "17:00-18:00";
EIGHTEEN_HOUR = "18:00-19:00";
NINETEEN_HOUR = "19:00-20:00";
TWENTY_HOUR = "20:00-21:00";
TWENTY_ONE_HOUR = "21:00-22:00";
TWENTY_TWO_HOUR = "22:00-23:00";
TWENTY_THREE_HOUR = "23:00-24:00";


TAG = 'BasePlantModel'

#所有植物模型的基类
class  BasePlant:

    totalGrowState = DEFAULT_TOTAL_GROW_STATE;

    nowGrowState = NO_GROW_STATE;

    nowGrowStateCode = NO_GROW_STATE_CODE;

    #actualTimeGrowFactor = GrowFactorModel.GrowFactor();#实时成长因素数据