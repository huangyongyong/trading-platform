import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.api import app
# 确保 Vercel 能找到 app 对象
app = app
# 不要在这里导入 app，而是定义一个函数，在运行