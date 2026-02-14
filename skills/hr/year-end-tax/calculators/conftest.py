"""
pytest conftest: calculators 디렉토리를 sys.path에 추가하여
하이픈 디렉토리(year-end-tax) 하위 모듈을 임포트할 수 있게 합니다.
"""
import sys
from pathlib import Path

# calculators 디렉토리를 sys.path에 추가
_calculators_dir = str(Path(__file__).resolve().parent)
if _calculators_dir not in sys.path:
    sys.path.insert(0, _calculators_dir)
