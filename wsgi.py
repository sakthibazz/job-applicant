import sys
import os

path = os.getcwd()
if path not in sys.path:
   sys.path.append(path)

from app import app as application