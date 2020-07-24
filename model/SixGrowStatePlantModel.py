#-*- coding:utf-8 -*-


import BasePlantModel;
import GrowFactorModel


FIRST_GROW_STATE_CODE = 1; #发芽期
SECOND_GROW_STATE_CODE = 2; #幼苗期
THIRD_GROW_STATE_CODE = 3; #生长期
FOURTH_GROW_STATE_CODE = 4; #开花期
FIVE_GROW_STATE_CODE = 5; #结果期
SIX_GROW_STATE_CODE = 6; # 采摘期

FIRST_GROW_STATE_NAME = '第一期'
SECOND_GROW_STATE_NAME = '第二期'
THIRD_GROW_STATE_NAME = '第三期'
FOURTH_GROW_STATE_NAME = '第四期'
FIVE_GROW_STATE_NAME = '第五期'
SIX_GROW_STATE_NAME = '第六期'

GROW_STATE = 'grow_state';

TAG = 'SixGrowStatePlantModel';

#生长期有6个阶段的植物
class SixGrowStatePlant(BasePlantModel.BasePlant):

    #对象里面的历史成长阶段数据
    firstHistoryGrowStateFactor = GrowFactorModel.GrowFactor;
    secondHistoryGrowStateFactor = GrowFactorModel.GrowFactor;
    thirdHistoryGrowStateFactor = GrowFactorModel.GrowFactor;
    fourthHistoryGrowStateFactor = GrowFactorModel.GrowFactor;
    fiveHistoryGrowStateFactor = GrowFactorModel.GrowFactor;
    sixHistoryGrowStateFactor = GrowFactorModel.GrowFactor;

    #实时成长数据
    actualTimeGrowFactor = GrowFactorModel.GrowFactor;

    #用于存储白天晚上不同成长阶段的最优值
    dayOptimalValue = {};
    nightOptimalValue = {};
    plantName = ''
    historyGrowStateList = [];

    #用于存储每小时的最优值，每组有24个
    firstGrowStateOptimalValue = [];
    secondGrowStateOptimalValue = [];
    thirdGrowStateOptimalValue = [];
    fourthGrowStateOptimalValue = [];
    fiveGrowStateOptimalValue = [];
    sixGrowStateOptimalValue = [];


    def __init__(self):
        print TAG + "  init";
        print self.nowGrowState;


    #def setNowGrowState(self, nowGrowState):
        #self.nowGrowState = nowGrowState;