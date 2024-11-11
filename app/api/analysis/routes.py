from utils import *
from . import analysis_bp
from flask import jsonify, request

from .chartHelper import *


##  仪表盘
@analysis_bp.route('/chart1', methods=['GET'])
def chart1():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)

    res = None

    try:
        if info["class_id"] is None:
            res = helper2(info["department_id"])
        else:
            res = helper1(info["class_id"])
    except:
        return get_500()

    if not res:
        return get_500()

    return jsonify({
        "code": 200,
        "data": res,
        "msg": "操作成功"
    })

## 堆叠柱状图
@analysis_bp.route('/chart2', methods=['GET'])
def chart2():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)

    res = None

    try:
        if info["class_id"] is None:
            res = helper4(info["department_id"])
            # pass
        else:
            res = helper3(info["class_id"])
    except:
        return get_500()

    if not res:
        return get_500()

    return jsonify({
        "code": 200,
        "data": res,
        "msg": "操作成功"
    })


## 状态分布雷达图
@analysis_bp.route('/chart3', methods=['GET'])
def chart3():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)

    res = None

    try:
        res = helper5()
    except:
        return get_500()

    if not res:
        return get_500()

    return jsonify({
        "code": 200,
        "data": res,
        "msg": "操作成功"
    })

## 状态分布饼图 最大
@analysis_bp.route('/chart4', methods=['GET'])
def chart4():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)

    res = None

    try:
        res = helper6()
    except:
        return get_500()

    if not res:
        return get_500()

    return jsonify({
        "code": 200,
        "data": res,
        "msg": "操作成功"
    })

## 状态分布饼图 最大
@analysis_bp.route('/chart5', methods=['GET'])
def chart5():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)

    res = None

    try:
        res = helper7()
    except:
        return get_500()

    if not res:
        return get_500()

    return jsonify({
        "code": 200,
        "data": res,
        "msg": "操作成功"
    })



## 获取异常
@analysis_bp.route('/getleaveserror', methods=['GET'])
def getleaveserror():
    pass
