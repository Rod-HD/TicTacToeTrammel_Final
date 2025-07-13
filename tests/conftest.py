# tests/conftest.py
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]   # thư mục gốc dự án
sys.path.append(str(root))                   # thêm vào sys.path
