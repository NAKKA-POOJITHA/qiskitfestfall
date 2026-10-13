import sys
from pathlib import Path

# Automatically add project root to sys.path for pytest
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
