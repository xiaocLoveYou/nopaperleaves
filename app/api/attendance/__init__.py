from flask import Blueprint

# 创建 temp 蓝本
attendance_bp = Blueprint('attendance', __name__)

# 导入 routes 文件来定义路由
from . import routes
