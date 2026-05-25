import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.api import app
# 确保 Vercel 能找到 app 对象
#app = app