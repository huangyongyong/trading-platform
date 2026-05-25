# api/index.py
import sys
from pathlib import Path

# 将项目根目录（api 的上一级）加入 Python 搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.api import app

# 确保 app 被导出
app = app