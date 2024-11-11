import os
from . import auth_bp
from flask import jsonify, request, current_app
from utils import *

@auth_bp.route('/upload', methods=['POST'])
def upload_file():
    """处理通过 FormData 上传的文件"""
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'message': '没有文件部分'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'fail', 'message': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        try:
            # 生成唯一的文件名
            unique_filename = generate_unique_filename(file.stream, file.filename)

            # 构建文件路径，使用 current_app.config
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

            # 保存文件
            file.save(file_path)

            return jsonify({
                'status': 'success',
                'message': '文件上传成功',
                'filename': unique_filename,
                'file_url': f"/uploads/{unique_filename}"
            }), 200
        except Exception as e:
            return jsonify({'status': 'fail', 'message': f'文件上传失败: {str(e)}'}), 500
    else:
        return jsonify({'status': 'fail', 'message': '不允许的文件类型'}), 400

# 用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    pass


# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 假设登录成功，返回一个令牌

    res = execute_sql_query(f"select * from users where username = %s and password = %s", (username, password))
    print(res)
    if len(res) == 0:
        return jsonify({"code": 500, "message": "登录失败, 用户不存在或密码错误"}), 200
    print(res)
    res = res[0]
    info = {
        "user_id": res["user_id"],
        "user_name": res["username"],
        "role": res["role"],
        "department_id": res["department_id"],
        "class_id": res["class_id"],
    }

    token: str = set_token(info)
    return jsonify({"code": 200, "message": "登录成功", "token": token}), 200


@auth_bp.route('/info', methods=['get'])
def info():
    authorization = get_Authorization(request)

    status, info = get_token(authorization)

    if not status:
        return get_401()

    print("token验证:", status, "用户信息:", info)
    return jsonify({
        "code": 200,
        "data": {
            "user_id": info["user_id"],
            "user_name": info["user_name"],
            "role": info["role"],
            "department_id": info["department_id"],
            "class_id": info["class_id"],
        },
        "msg": "操作成功"
    }), 200

