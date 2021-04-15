'''
import requests, sys
import datetime, timedelta

urlPost = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000/engine/mandelbrot?max_iter=700&width=700&height=700"
urlGet = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000"

def call_request_get(count):
    res = requests.get(urlGet) 
    print("Call " + str(count+1) + " on "+urlGet+" : " + str(res.status_code))

def call_request_post(count):
    res = requests.post(urlPost) 
    print("Call " + str(count+1) + " on "+urlPost+" : " + str(res.status_code))

try:
    for i in range(int(sys.argv[1])):
        if sys.argv[2] == "post":
            call_request_post(i)   
        if sys.argv[2] == "get":
            call_request_get(i)  
except:
    minutes = sys.argv[1].split("min")
    finish_time = datetime.datetime.now() + datetime.timedelta(minutes=int(minutes[0]))
    i = 0
    while datetime.datetime.now() < finish_time:
        if sys.argv[2] == "post":
            call_request_post(i)   
        if sys.argv[2] == "get":
            call_request_get(i)
        i+=1

'''

import asyncio, datetime, sys
import requests

auto_scaling_group = "os.environ['AUTO_SCALING_GROUP']"
region = "os.environ['REGION']"
accessKeyId = "os.environ['ACCESS_KEY']"
secretAccessKey = "os.environ['SECRET_KEY']"
sessionToken = "os.environ['SESSION_TOKEN']"
env = "dev" #os.environ['ENV']

class Run:

    def __init__(self):        
        self._urlPost = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000/engine/mandelbrot?max_iter=1000&width=1000&height=1000"
        self._urlGet = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000"

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
    