#-*- coding:utf-8 -*-


from BasePlantModel import BasePlant as BasePlant;
from SixGrowStatePlantModel import SixGrowStatePlant as SixGrowStatePlant;

#大棚基础类，默认大棚编号，种植作物编号为0，创建时，具体赋值

TAG = 'BaseHouseModel'

DEFAULT_HOUSE_CODE = 0;
DEFAULT_PLANT_CODE = 0;

class BaseHouse:

    houseCode = DEFAULT_HOUSE_CODE;
    plantCode = DEFAULT_PLANT_CODE;

    houseName = '';
    #大棚里面的植物，暂时默认创建具有6个生长阶段的植物
    #plant = SixGrowStatePlantModel()

   #大棚里面的设备情况列表
    houseActorList = [];

    def __init__(self):
        print TAG + "  init"

    def setHouseCode(self, house_code):
        self.houseCode = house_code;

    def setPlantCode(self, plant_code):
        self.plantCode = plant_code;

    def setPlant(self, plantInHouse):
        self.plant = plantInHouse;

    def setHouseName(self, name):
        self.houseName = name;