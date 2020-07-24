#-*- coding:utf-8 -*-




#大棚设备状况

TAG = 'BaseActorModel';

class BaseActorModel:

    #默认动作器编号，大棚编号等为 0， 表示没有
    actorCode = 0;
    greenHouseCode = 0;
    actorModeName = ''; #设备状态名称, 初始化为空， 由于数据库中取名为actorModeName，因此本类取名为 actorModeName;
    def __init__(self):
        print TAG + '   init';

    def setBaseActor(self, code):
        self.actorCode = code;

    def setGreenHouseCode(self, code):
        self.greenHouseCode = code;

    #设置设备的工作状态，
    def setDeviceState(self, state):
        self.actorModeName = state;