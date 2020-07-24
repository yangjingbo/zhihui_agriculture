#-*- coding:utf-8 -*-
import sys
from  lib.bottle.bottle import route, Bottle, run, request,response
from lib.mysqlconnector.lib.mysql import connector
from lib.pymysql import pymysql
#from lib.Mysql import MySQLdb
import traceback
import json
from DBUtils.PooledDB import PooledDB,SharedDBConnection
import Conf as Conf
from Util.CustomDbUtil import POOL as POOL
from model.BaseHouseModel import BaseHouse as BaseHouse;
from model.BasePlantModel import BasePlant as BasePlant;
from model.SixGrowStatePlantModel import SixGrowStatePlant as SixGrowStatePlant;
from model import GrowFactorModel as GrowFactorModel;
import model.SixGrowStatePlantModel as SixGrowStatePlantModel;
import model.ActorModel as ActorModel;

hiddenimports=['mysql','mysql.connector.locales.eng.client_error']
hiddenimports=['lib.mysqlconnector.lib.mysql','lib.mysqlconnector.lib.mysql.connector.locales.eng.client_error']
reload(sys)
sys.setdefaultencoding("utf-8")


#sqlOptimalFactor = 'SELECT T1.*,T2.GrowthModelName,T3.GrowthPhaseName,T4.DayorNightName,T5.TimePeroidName FROM PGM_BestParameter T1 LEFT OUTER JOIN PGM_ModelInfo T2 ON T1.GrowthModelCode=T2.GrowthModelCode LEFT OUTER JOIN DIC_GrowthPhase T3 ON T1.GrowthPhaseCode=T3.GrowthPhaseCode LEFT OUTER JOIN DIC_DayorNight T4 ON T1.DayOrNight=T4.DayorNightCode LEFT OUTER JOIN DIC_TimePeriod T5 ON T1.TimePeroidCode=T5.TimePeroidCode'

app = Bottle()


@app.route('/updateOperationFarmRecord')
def updateOperationFarmRecord():
    print 'update operation farm order'

    houseCode = request.query.house_code;
    time = request.query.time;
    desc = request.query.desc;
    result = updateOperationFarmRecordInDb(houseCode, time, desc);
    response.headers["Access-Control-Allow-Origin"] = "*"
    return 'ok';



@app.route('/updateOperationOrder')
def updateOperationOrder():
    print 'update operation order'

    houseCode = request.query.house_code;
    actorCode = request.query.actor_code;
    actorAction = request.query.action;
    operateTime = request.query.time;
    result = updateOrderInDb(houseCode, actorCode, actorAction, operateTime);
    response.headers["Access-Control-Allow-Origin"] = "*"
    return 'ok';



#result[j][0]表示actorCode, result[j][1]设备名称， ,result[j][2]表示大棚编码, result[j][16]表示设备状态
@app.route('/getDeviceState')
def getDeviceState():
    houseCode = request.query.house_code;
    houseArray = houseCode.split(',');
    result = selectDeviceStateInfo(houseCode);
    responseInfoList = [];
    for i in range(0, len(houseArray)):
        house = BaseHouse();
        house.houseCode = houseArray[i];
        house.houseActorList = [];
        responseInfoList.append(house);
        for j in range(0, len(result)):
            if(houseArray[i] == str(result[j][2])):
                actor = ActorModel.BaseActorModel();
                actor.actorCode = result[j][0];
                actor.actorModeName = result[j][16];
                house.houseActorList.append(actor);
                print  result[j][0], result[j][1],result[j][2], result[j][16];

    response.headers["Access-Control-Allow-Origin"] = "*"
    jsonObjResult = json.dumps(responseInfoList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4, ensure_ascii=False);
    return  jsonObjResult;#json.dumps('普法', ensure_ascii = False)


#获取植物现在处在的成长阶段，参数为house_code, 可以传一个大棚code，也可以传多个，多个之间使用英文逗号','隔开
@app.route('/getNowGrowState')
def getPlantNowGrowNowInfo():
    houseCode = request.query.house_code
    houseArray = houseCode.split(',');  #
    result = selectNowGrowStateInfo(houseCode);  # 从数据库查询的结果
    responseHouseInfoList = [];  # 存储大棚，每个大棚具有相应的植物生长信息
    for i in range(0, len(houseArray)):
        house = BaseHouse();
        house.houseCode = houseArray[i];
        plant = SixGrowStatePlant();#默认六个成长期的植物,后续可以拓展，如果数据库里面有总的植物成长阶段字段，根据此字段创建不同的plant
        house.setPlant(plant);
        responseHouseInfoList.append(house);
        for j in range(0, len(result)):
            if(houseArray[i] == str(result[j][0])):
                plant.nowGrowState = result[j][7];
                plant.nowGrowStateCode = result[j][6];
                house.plantCode = result[j][2];

    response.headers["Access-Control-Allow-Origin"] = "*"
    jsonObjResult = json.dumps(responseHouseInfoList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4, ensure_ascii=False);
    return  jsonObjResult;#json.dumps('普法', ensure_ascii = False)


@app.route('/getPlantHourOptimalValue')
def getPlantHourOptimalInfo():
    print 'get hour optimal value---------------'
    plantCodes = request.query.plant_code;
    result = selectPlantHourOptimalFactor(plantCodes)
    plantsArray = plantCodes.split(',');
    responsePlantInfoList = [];  # 存储植物最右生长要素信息
    for i in range(0, len(plantsArray)):
        house = BaseHouse();
        house.plantCode = plantsArray[i];
        plant = SixGrowStatePlant();
        plant.firstGrowStateOptimalValue = [];
        plant.secondGrowStateOptimalValue = [];
        plant.thirdGrowStateOptimalValue = [];
        plant.fourthGrowStateOptimalValue = [];
        plant.fiveGrowStateOptimalValue = [];
        plant.sixGrowStateOptimalValue = [];
        house.setPlant(plant);
        responsePlantInfoList.append(house);
        print 'hour: ', result[i][8];
        for j in range(0, len(result)):
            if (plantsArray[i] == str(result[j][1])):#判断植物编码是否想等
                plant.plantName = result[j][5];
                growFactor = GrowFactorModel.GrowFactor();
                growFactor.guang = result[j][10];
                growFactor.wendu = result[j][11];
                growFactor.shidu = result[j][12];
                growFactor.ec = result[j][13];
                growFactor.co2 = result[j][14];
                growFactor.soilwendu = result[j][15];
                growFactor.soilshidu = result[j][16];
                growFactor.day_time = result[j][8];
                growFactor.now_hour = result[j][9];#小时时间段
                # growFactor.grow_state_code = 表里面暂时没有成长阶段对应的编码
                if (result[j][7] == SixGrowStatePlantModel.FIRST_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.firstGrowStateOptimalValue.append(growFactor);
                if (result[j][7] == SixGrowStatePlantModel.SECOND_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.secondGrowStateOptimalValue.append(growFactor);
                if (result[j][7] == SixGrowStatePlantModel.THIRD_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.thirdGrowStateOptimalValue.append(growFactor);
                if (result[j][7] == SixGrowStatePlantModel.FOURTH_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.fourthGrowStateOptimalValue.append(growFactor);
                if (result[j][7] == SixGrowStatePlantModel.FIVE_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.fiveGrowStateOptimalValue.append(growFactor);
                if (result[j][7] == SixGrowStatePlantModel.SIX_GROW_STATE_NAME):
                    growFactor.grow_state = result[j][7];
                    plant.sixGrowStateOptimalValue.append(growFactor);

    response.headers["Access-Control-Allow-Origin"] = "*"
    jsonObjResult = json.dumps(responsePlantInfoList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
                               ensure_ascii=False);
    return jsonObjResult;



def setPlantFactorValue(factorModel, factorCode, value):
    print 'set plant factor code*******************: ',factorCode
    if(factorCode == GrowFactorModel.GUANG_FACTOR_CODE):
        print 'guang ********************';
        factorModel.guang = value;

    if (factorCode == GrowFactorModel.WEN_DU_FACTOR_CODE):
        factorModel.wendu = value;

    if (factorCode == GrowFactorModel.SHI_DU_FACTOR_CODE):
        factorModel.shidu = value

    if (factorCode == GrowFactorModel.EC_FACTOR_CODE):
        factorModel.ec = value;

    if (factorCode == GrowFactorModel.CO2_FACTOR_CODE):
        factorModel.co2 = value;

    if (factorCode == GrowFactorModel.SOIL_WEN_DU_FACTOR_CODE):
        factorModel.soilwendu = value;

    if (factorCode == GrowFactorModel.SOIL_SHI_DU_FACTOR_CODE):
        factorModel.soilshidu = value;

#获取大棚内植物成长历史的数据，根据houseCode查，可以有多个house_code参数，不同house_code用英文逗号','分开
@app.route('/getGrowStateHistoryInfo')
def getPlantGrowHistoryInfo():
    houseCodes = request.query.house_code;
    houseArray = houseCodes.split(',');
    result = selectPlantGrowStateHistoryInfo(houseCodes)
    houseGrowStateInfoList = [];
    for i in range(0, len(houseArray)):
        house = BaseHouse();
        house.houseCode = houseArray[i];
        plant = SixGrowStatePlant();#成长阶段有6个的植物，后续如果有其他成长阶段的植物，可以根据数据库中的字段进行修改，数据库以后可以增加该字段,代码可以后续优化
        plant.firstHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        plant.secondHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        plant.thirdHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        plant.fourthHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        plant.fiveHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        plant.sixHistoryGrowStateFactor = GrowFactorModel.GrowFactor();
        house.setPlant(plant);
        houseGrowStateInfoList.append(house);
        for j in range(0, len(result)):
            if(houseArray[i] == str(result[j][1])):
                house.houseName = result[j][6];
                value = str(format((result[j][11]), '.1f'));
                if(result[j][2] == SixGrowStatePlantModel.FIRST_GROW_STATE_CODE):
                    plant.firstHistoryGrowStateFactor.grow_state = result[j][7];
                    plant.firstHistoryGrowStateFactor.grow_state_code = result[j][2];
                    setPlantFactorValue(plant.firstHistoryGrowStateFactor, result[j][4], value);

                if (result[j][2] == SixGrowStatePlantModel.SECOND_GROW_STATE_CODE):
                    plant.secondHistoryGrowStateFactor.grow_state = result[j][7];
                    plant.secondHistoryGrowStateFactor.grow_state_code = result[j][2];
                    setPlantFactorValue(plant.secondHistoryGrowStateFactor, result[j][4], value);

                if (result[j][2] == SixGrowStatePlantModel.THIRD_GROW_STATE_CODE):
                    plant.thirdHistoryGrowStateFactor.grow_state = result[j][7];
                    plant.thirdHistoryGrowStateFactor.grow_state_code = result[j][2];
                    setPlantFactorValue(plant.thirdHistoryGrowStateFactor, result[j][4], value);

                if (result[j][2] == SixGrowStatePlantModel.FOURTH_GROW_STATE_CODE):
                    plant.fourthHistoryGrowStateFactor.grow_state = result[j][7];
                    plant.fourthHistoryGrowStateFactor.grow_state_code = result[j][2];
                    setPlantFactorValue(plant.fourthHistoryGrowStateFactor, result[j][4], value);

                if (result[j][2] == SixGrowStatePlantModel.FIVE_GROW_STATE_CODE):
                    plant.fiveHistoryGrowStateFactor.grow_state = result[j][7];
                    plant.fiveHistoryGrowStateFactor.grow_state_code = result[j][2];
                    setPlantFactorValue(plant.fiveHistoryGrowStateFactor, result[j][4], value);


    response.headers["Access-Control-Allow-Origin"] = "*"
    # print result[0][1], result[0][2],result[0][6],result[0][15],result[0][17]
    jsonObjResult = json.dumps(houseGrowStateInfoList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
                               ensure_ascii=False);

    return jsonObjResult;  # json.dumps(responseHouseInfoList, ensure_ascii = False);



#参数传 housecode
@app.route('/getHouseFarmingRecord')
def getFarmingRecord():
    houseCode = request.query.housecode
    response.headers["Access-Control-Allow-Origin"] = "*"
    result = selectFarmingRecord(houseCode)
    list = []
    for i in range(0, len(result)):
        list.append(result[i][2])
    dict = {'housecode':houseCode, 'records':list}
    return json.dumps(dict, ensure_ascii = False)


#参数传 housecode
@app.route('/getHouseAlarmingRecord')
def getAlarmingRecord():
    houseCode = request.query.housecode
    response.headers["Access-Control-Allow-Origin"] = "*"
    result = selectAlarmingRecord(houseCode)
    list = []
    for i in range(0, len(result)):
        list.append(result[i][2])
    dict = {'housecode':houseCode, 'records':list}
    return json.dumps(dict, ensure_ascii = False)

#参数为大棚编号，可以传递多个编号，不同编号之间使用英文逗号','隔开
@app.route('/getAllPlantsOptimalFactors')
def getAllPlantOptimalFactors():
    plantCodes = request.query.plant_code;
    print plantCodes;
    plantsArray = plantCodes.split(',');
    result = selectAllPlantsOptimalFactor(plantCodes);
    responsePlantInfoList = [];  # 存储植物最右生长要素信息
    for i in range(0, len(plantsArray)):
        house = BaseHouse();
        house.plantCode = plantsArray[i];
        plant = SixGrowStatePlant();
        plant.dayOptimalValue = [];
        plant.nightOptimalValue = [];
        house.setPlant(plant);
        responsePlantInfoList.append(house);
        for j in range(0, len(result)):
            if(plantsArray[i] == str(result[j][1])):
                plant.plantName = result[j][5];
                growFactor = GrowFactorModel.GrowFactor();
                growFactor.guang = result[j][10];
                growFactor.wendu = result[j][11];
                growFactor.shidu = result[j][12];
                growFactor.ec = result[j][13];
                growFactor.co2 = result[j][14];
                growFactor.soilwendu = result[j][15];
                growFactor.soilshidu = result[j][16];
                growFactor.grow_state = result[j][7];
                growFactor.day_time = result[j][8];
                #growFactor.grow_state_code = 表里面暂时没有成长阶段对应的编码
                if (result[j][2] == GrowFactorModel.DAY_CODE):
                    plant.dayOptimalValue.append(growFactor);
                else:
                    plant.nightOptimalValue.append(growFactor);

    response.headers["Access-Control-Allow-Origin"] = "*"
    jsonObjResult = json.dumps(responsePlantInfoList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,ensure_ascii=False);
    return jsonObjResult;


# python plant_model_server.py,
#获取成长信息，最佳PH，CO2 实际PH，CO2等值
#传递参数 house_code 可以为一个，也可以为多个，多个直接用英文逗号','分开
@app.route('/getActualTimeGrowinfo')
def getActualTimeGrowInfo():
    houseCode = str(request.query.house_code);
    houseArray= houseCode.split(',');#
    print  len(houseArray);
    result = selectActualTimeGrowInfo(houseCode);#从数据库查询的结果
    responseHouseInfoList = [];# 存储大棚，每个大棚具有相应的植物生长信息
    for i in range(0, len(houseArray)):#创建相应数量的大棚
        plant = SixGrowStatePlant();#默认为有6个成长阶段的植物，后续考虑数据库添加具有多少成长阶段的字段，通过查询的值，具体创建几个成长阶段的植物
        plant.actualTimeGrowFactor = GrowFactorModel.GrowFactor();
        house = BaseHouse();
        house.houseCode = houseArray[i];
        house.setPlant(plant);
        responseHouseInfoList.append(house);
        for j in range(0, len(result)):#遍历result，将结果放入对应的大棚
            if (str(result[j][1]) == houseArray[i]):
                #print 'result  equals ---------------',result[j][6]
                #house.plantCode = result[i][6];数据库中如果有对应植物编号，则在此设置plantCode
                #plant.actualTimeGrowFactor.grow_state_code =
                if(result[j][6] == GrowFactorModel.GUANG_FACTOR_CODE):
                    plant.actualTimeGrowFactor.guang = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.WEN_DU_FACTOR_CODE):
                    plant.actualTimeGrowFactor.wendu = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.SHI_DU_FACTOR_CODE):
                    plant.actualTimeGrowFactor.shidu = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.EC_FACTOR_CODE):
                    plant.actualTimeGrowFactor.ec = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.CO2_FACTOR_CODE):
                    plant.actualTimeGrowFactor.co2 = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.SOIL_WEN_DU_FACTOR_CODE):
                    plant.actualTimeGrowFactor.soilwendu = str(format(result[j][19],'.1f'));

                if (result[j][6] == GrowFactorModel.SOIL_SHI_DU_FACTOR_CODE):
                    plant.actualTimeGrowFactor.soilshidu = str(format(result[j][19],'.1f'));

    response.headers["Access-Control-Allow-Origin"] = "*"
    #print result[0][1], result[0][2],result[0][6],result[0][15],result[0][17]
    jsonObjResult = json.dumps(responseHouseInfoList, default = lambda obj:obj.__dict__, sort_keys = True, indent = 4, ensure_ascii = False);

    return jsonObjResult;#json.dumps(responseHouseInfoList, ensure_ascii = False);


def selectFarmingRecord(code):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        #cursor.execute('select * from  '+ farmingRecordTable + '  where GreenhouseCode= %s '+' order by ALARMDATE desc limit 8',(code))
        cursor.execute('SELECT * FROM v_di_worktask where GreenhouseCode=%s order by JournalDate desc limit 8',code)
        values = cursor.fetchall()
        return values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


def selectAlarmingRecord(code):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        #cursor.execute('select * from  '+ farmingRecordTable + '  where GreenhouseCode= %s '+' order by ALARMDATE desc limit 8',(code))
        cursor.execute('SELECT * FROM v_di_alarm where GreenhouseCode=%s order by ALARMDATE desc limit 8',code)
        values = cursor.fetchall()
        return values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


def selectActualTimeGrowInfo(houseCode):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        print (houseCode)
        #cursor.execute('select * from ' + Conf.plantActualTimeGrowInfoTable + ' where greenhousecode in(1001,1002,1003,1004)')
        cursor.execute("select * from  " + Conf.plantActualTimeGrowInfoTable + " where greenhousecode in({})".format(houseCode))
        values = cursor.fetchall()
        #for d in values:
            #print d[0], d[1], d[2], d[3], d[4], d[5],d[6],d[7],d[8],d[9]
        return values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectNowGrowStateInfo(houseCode):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        #cursor.execute('select * from ' + Conf.nowGrowStateTable + ' where greenhousecode in(1001,1002,1003,1004)')
        cursor.execute("select * from  " + Conf.nowGrowStateTable + " where greenhousecode in({})".format(houseCode))
        values = cursor.fetchall()
        return values
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectFromInfoTable():
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        cursor.execute('select * from '+ Conf.greenHouseInfoTable)
        values = cursor.fetchall()
        return values
        #print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectGrowInfoFromTable():
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        cursor.execute('select * from '+Conf.plantBestGrowInfoTable)
        values = cursor.fetchall()
        #for d in values:
            #print d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12],d[13],d[14],d[15]
        return values
    except Exception as e:
        print "get grow optimal Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectAllPlantsOptimalFactor(plantCodes):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        #cursor.execute('select * from ' + Conf.allPlantsOptimalTable)
        cursor.execute("select * from  " + Conf.allPlantsOptimalTable + " where growthmodelcode in({})".format(plantCodes))
        values = cursor.fetchall()
        #for d in values:
         #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13], d[14]
        return values
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectPlantHourOptimalFactor(plantCodes):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        #cursor.execute('select * from ' + Conf.allPlantsOptimalTable)
        cursor.execute("select * from  " + Conf.plantHourOptimalTable + " where growthmodelcode in({})".format(plantCodes))
        values = cursor.fetchall()
        #for d in values:
         #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13], d[14]
        return values
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectPlantGrowStateHistoryInfo(houseCodes):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        #cursor.execute('select * from ' + Conf.plantHistoryGrowInfoTable );
        cursor.execute("select * from  " + Conf.plantHistoryGrowInfoTable + " where greenhousecode in({})".format(houseCodes))
        values = cursor.fetchall();
        #for d in values:
        #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7],d[8],d[9],d[10],d[11]
        return values
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def selectDeviceStateInfo(houseCodes):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        # cursor.execute('select * from ' + Conf.plantHistoryGrowInfoTable );
        cursor.execute("select * from  " + Conf.deviceStateTable + " where greenhousecode in({})".format(houseCodes))
        values = cursor.fetchall();
        # for d in values:
        #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7],d[8],d[9],d[10],d[11]
        return values;
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def updateOrderInDb(houseCode, actorCode, action, time):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        # cursor.execute('select * from ' + Conf.plantHistoryGrowInfoTable );
        #insert into data_order(GreenhouseCode,ActorCode,ActionCode,ActionParameter1 VALUES
        orderFormat = "({0},{1},{2},{3})";
        values = str.format(orderFormat, houseCode, actorCode, action, time);
        print values;
        sql = 'insert into  data_order (GreenHouseCode, ActorCode, ActionCode, actionParameter1) values  ' + values ;
        print sql;
        #cursor.execute('insert into  data_order (GreenHouseCode, ActorCode, ActionCode, ) values  (1001)' );
        cursor.execute(sql);
        conn.commit();
        #values = cursor.fetchall();
        # for d in values:
        #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7],d[8],d[9],d[10],d[11]
        #return values;
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

def updateOperationFarmRecordInDb(houseCode, time, desc):
    conn = POOL.connection();
    cursor = conn.cursor();
    try:
        # cursor.execute('select * from ' + Conf.plantHistoryGrowInfoTable );
        # insert into data_order(GreenhouseCode,ActorCode,ActionCode,ActionParameter1 VALUES
        recordFormat = "({0},'{1}','{2}')";
        values = str.format(recordFormat, houseCode, str(time), str(desc));
        print values;
        #sql = 'insert into  data_order (GreenHouseCode, ActorCode, ActionCode, actionParameter1) values  ' + values;
        sql = "insert into Journal_WorkTask (GreenhouseCode,JournaTime,JournaContent) values "+ values;
        print sql;
        # cursor.execute('insert into  data_order (GreenHouseCode, ActorCode, ActionCode, ) values  (1001)' );
        cursor.execute(sql);
        conn.commit();
        # values = cursor.fetchall();
        # for d in values:
        #   print d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7],d[8],d[9],d[10],d[11]
        # return values;
        # print values
    except Exception as e:
        print "Exception: " + traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    print 'run main'
    run(app, host = Conf.serverIp, port = Conf.serverPort)
