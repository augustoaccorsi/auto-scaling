
import asyncio, datetime, sys
import requests
from random import seed
from random import randint
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Run:

    def __init__(self):        
        self._urlPost = "http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000/engine/mand?max_iter=950&width=950&height=950"
        self._urlGet = "http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000"

    def call_request_get(self, count):
        res = requests.get(self._urlGet) 
        print("Call " + str(count+1) + " on "+self._urlGet+" : " + str(res.status_code))
        return res.status_code

    def call_request_post(self, count):
        res = requests.post(self._urlPost) 
        print("Call " + str(count+1) + " on "+self._urlPost.replace("http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000","")+" on "+str(datetime.datetime.now())+" : "+ str(res.status_code))
        return res.status_code
        
    async def call_url(self, type):
        #await asyncio.sleep(600)
        count = 0
        while True:
            minutes = randint(0, 20)
            sleep = (randint(10, 20) * 60)
            print("calls: "+str(minutes))
            print("sleep: "+str(sleep/60))
            exit_code = 0
            finish_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            while datetime.datetime.now() < finish_time:
                if type == "post":
                    status_code = self.call_request_post(count)   
                if type == "get":
                    status_code = self.call_request_get(count)
                if status_code != 201:
                    exit_code+=1
                if exit_code == 15:
                    exit_code = 0
                    break
                count+=1
            print("----------------------------------")
            await asyncio.sleep(sleep)

if __name__ == '__main__':
    run = Run()
    print("Starting Event Loop")
    loop = asyncio.get_event_loop()
    try:
        print("----------------------------------")
        try:
            if sys.argv[1] == "post":
                asyncio.ensure_future(run.call_url("post"))
            if sys.argv[1] == "get":
                asyncio.ensure_future(run.call_url("get"))
        except:
            for i in range(int(sys.argv[1])):
                if sys.argv[2] == "post":
                    run.call_request_post(i)
                else:
                    run.call_request_get(i)
            pass
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Event Loop")
        loop.close()

'''
class Run:

    def __init__(self):        
        #self._urlPost = "http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000/engine/mand?max_iter=850&width=850&height=850"
        self._urlPost = "http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000/engine/mand?max_iter=1000&width=1000&height=1000"
        self._urlGet = "http://augusto-accorsi-engine-elb-1884692720.sa-east-1.elb.amazonaws.com:5000"

    def call_request_get(self, count):
        res = requests.get(self._urlGet)
        print("Call " + str(count+1) + " on "+self._urlGet+" : " + str(res.status_code))
    def call_request_post(self, count):
        res = requests.post(self._urlPost)
        print("Call " + str(count+1) + " on "+self._urlPost+" : " + str(res.status_code))
        
    async def call_url(self, type, minutes):
        count = 0
        while True:
            finish_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            while datetime.datetime.now() < finish_time:
                if type == "post":
                    self.call_request_post(count)  
                if type == "get":
                    self.call_request_get(count)
                count+=1
            print("----------------------------------")
            await asyncio.sleep(1200)
if __name__ == '__main__':
    run = Run()
    print("Starting Event Loop")
    loop = asyncio.get_event_loop()
    try:
        print("----------------------------------")
        asyncio.ensure_future(run.call_url("post", 10))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Event Loop")
        loop.close()    
'''