
import asyncio, datetime, sys
import requests
from random import seed
from random import randint
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

def call_database(count):
    url = 'http://augusto-accorsi-webapp-elb-1925434936.sa-east-1.elb.amazonaws.com:3001/database/save'
    session = requests.Session()
    session.trust_env = False
    res = session.post(url=url, files={'image': ('file.PNG', 'image.png', 'image/png')})
    print("Call " + str(count+1) + " on /database/save on "+str(datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))+" : "+ str(res.status_code))

call_database(1)