import os
import sys

# Add project root to sys.path for module imports
root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if root not in sys.path:
    sys.path.insert(0, root)
