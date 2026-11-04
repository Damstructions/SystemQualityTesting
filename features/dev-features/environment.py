import os
import sys

# Behave only executes environment.py. The OpenCart hooks live in
# environment2.py so the DemoBlaze hook under features/ stays untouched.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from environment2 import after_all, after_scenario, before_all, before_scenario  # noqa: E402
