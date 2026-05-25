# 原来的：from app.api import app

# 修改方案 A：尝试直接从上级目录导入（推荐先试这个）
import sys
import os

# 将项目根目录添加到 Python 搜索路径的最前面
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 现在再尝试导入
try:
    from app.api import app
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current sys.path: {sys.path}")
    raise e