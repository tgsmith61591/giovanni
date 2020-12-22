# -*- coding: utf-8 -*-

from pathlib import Path

try:
    version_path = Path(__file__).parent / 'VERSION'
    version = version_path.read_text().strip()
except FileNotFoundError:
    version = '0.0.0'

__version__ = version
del version
