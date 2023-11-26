import sys, os.path
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from db import *
import json

def test_db_top_users_all():
    file='{}'
    pass
    #js = json.loads(db_top_users_all(js_file))
    #assert js == str({'bob','alice','mike'})