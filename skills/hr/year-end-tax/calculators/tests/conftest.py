"""
conftest.py for calculators tests.

Adds the calculators directory to sys.path so tests can import
modules despite the parent directory containing hyphens (year-end-tax).
"""

import sys
from pathlib import Path

_calculators_dir = str(Path(__file__).resolve().parent.parent)
if _calculators_dir not in sys.path:
    sys.path.insert(0, _calculators_dir)
