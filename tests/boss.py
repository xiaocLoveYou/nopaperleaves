import pymysql
from pymysql import MySQLError

def execute_insert_query(query, params):
    connection = None
    success = False
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="nopaper"
        )

        with connection.cursor() as cursor:
            cursor.executemany(query, params)
            connection.commit()
            success = cursor.rowcount > 0

    except MySQLError as e:
        print(f"数据库错误类型: {type(e)}")
        print(f"数据库错误信息: {e}")
        success = False
    except Exception as e:
        print(f"其他错误类型: {type(e)}")
        print(f"错误信息: {e}")
        success = False
    finally:
        if connection:
            connection.close()

    return success

query = """
INSERT INTO attendance (username, date, status, department_id, resion, class_id) 
VALUES (%s, %s, %s, %s, %s, %s)
"""

params = [
    ("信息系", "2024-11-01", "1", 4, None, 1233),
    ("财经系", "2024-11-01", "2", 3, "请假", 1229),
    ("中餐系", "2024-11-02", "1", 1, "出差", None),
]

success = execute_insert_query(query, params)
print("批量插入成功" if success else "批量插入失败")
