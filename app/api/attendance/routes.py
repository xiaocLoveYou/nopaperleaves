from time import sleep

from utils import *
from . import attendance_bp
from flask import jsonify, request

# 获取考勤记录
@attendance_bp.route('/attendancelist', methods=['GET'])
def attendancelist():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)
    s_sql = ""
    data = ()
    if info["role"] == "normal":
        s_sql = """
                select * from attendance where user_id = %s
            """
        data = (info["user_id"])
    elif info["role"] == "teacher":
        s_sql = """
                select * from attendance where class_id = %s
            """
        data = (info["class_id"])
    elif info["role"] == "manager":
        s_sql = """
                select * from attendance where department_id = %s
            """
        data = (info["department_id"])
    elif info["role"] == "admin":
        pass

    results = execute_sql_query(s_sql, data)

    print("获取数据：", results)

    if not results:
        return get_500()

    return jsonify({
        "code": 200,
        "data": results,
        "msg": "操作成功",
    })

# 获取今天考勤记录
@attendance_bp.route('/todayattendancelist', methods=['GET'])
def todayattendancelist():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)
    s_sql = ""
    data = ()

    if info["role"] == "normal":
        s_sql = """
                select * from attendance where user_id = %s and `date` = %s
            """
        data = (info["user_id"], get_local_date())
    elif info["role"] == "teacher":
        print("==========teacher==========")
        s_sql = """
                select * from attendance where class_id = %s and `date` = %s
            """
        data = (info["class_id"], get_local_date())
    elif info["role"] == "manager":
        s_sql = """
                select * from attendance where department_id = %s and `date` = %s
            """
        data = (info["department_id"], get_local_date())
    elif info["role"] == "admin":
        pass

    results = execute_sql_query(s_sql, data)

    print("获取数据：", results)

    if not results:
        return get_500()

    return jsonify({
        "code": 200,
        "data": results,
        "msg": "操作成功",
    })

# 获取学生
@attendance_bp.route('/getstudent', methods=['GET'])
def getstudent():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)
    s_sql = ""
    data = ()
    if info["role"] == "normal":
        return get_403()
    elif info["role"] == "teacher":
        s_sql = """
                select * from users where class_id = %s
            """
        data = (info["class_id"])
    elif info["role"] == "manager":
        s_sql = """
                select * from users where department_id = %s
            """
        data = (info["department_id"])
    elif info["role"] == "admin":
        pass

    results = execute_sql_query(s_sql, data)

    print("获取数据：", results)

    if not results:
        return get_500()

    return jsonify({
        "code": 200,
        "data": results,
        "msg": "操作成功",
    })

# 老师提交当前全班考勤
@attendance_bp.route('/classattendance', methods=['POST'])
def classattendance():
    authorization = get_Authorization(request)
    status, info = get_token(authorization)

    class_id = info["class_id"]
    department_id = info["department_id"]

    print("token验证:", status, "用户信息:", info)
    data = request.get_json()
    print(data)
    user_ids = data.get('user_ids')
    statuses = data.get('statuses')
    resions = data.get('resions')
    date = data.get('date')
    role = info['role']


    if not status:
        return get_401()

    if role == "normal" and role == "manager":
        return get_403()

    res = execute_update_query("DELETE FROM attendance WHERE date = %s and class_id = %s and department_id = %s", (date, class_id, department_id))
    print(res)
    # if not res:
    #     return get_500()

    s_sql = "insert into attendance(user_id, date, status, department_id, resion, class_id) values(%s, %s, %s, %s, %s, %s)"
    data = []

    for user_id, status, resion in zip(user_ids, statuses, resions):
        print(user_id, date, status, department_id, resion, class_id)
        data = (
            user_id, date, str(status), department_id, resion, class_id
        )
        print(data)
        results = execute_insert_query(s_sql, data)
        #
        # print("获取数据：", results)
        #
        if not results:
            return get_500()
        #

    print(data)

    #

    return jsonify({
        "code": 200,
        "msg": "操作成功",
    })

# 学生提交请假申请
@attendance_bp.route('/studentcreateleavve', methods=['POST'])
def studentcreateleavve():
    authorization = get_Authorization(request)
    status, info = get_token(authorization)

    class_id = info["class_id"]
    department_id = info["department_id"]

    print("token验证:", status, "用户信息:", info)
    s_sql = "insert into attendance(user_id, date, status, department_id, resion, class_id) values(%s, %s, %s, %s, %s, %s)"



    data = request.get_json()
    print(data)
    user_id = data.get('user_ids')
    statuse = data.get('statuses')
    resions = data.get('resions')
    date = data.get('date')
    role = info['role']
    data = []

    if not status:
        return get_401()

    if role == "teacher" and role == "manager":
        return get_403()


    return jsonify({
        "code": 200,
        "msg": "操作成功",
    })

