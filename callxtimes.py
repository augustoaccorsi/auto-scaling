import asyncio, datetime, sys
import requests
from random import seed
from random import randint

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
        
    async def call_url(self, type):
        count = 0
        while True:
            minutes = randint(1, 20)
            sleep = (randint(1, 20) * 60)
            print("calls: "+str(minutes))
            print("sleep: "+str(sleep))
            finish_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            while datetime.datetime.now() < finish_time:
                if type == "post":
                    self.call_request_post(count)   
                if type == "get":
                    self.call_request_get(count)
                count+=1
            print("----------------------------------")
            await asyncio.sleep(sleep)

if __name__ == '__main__':
    run = Run()
    print("Starting Event Loop")
    loop = asyncio.get_event_loop()
    try:
        print("----------------------------------")
        asyncio.ensure_future(run.call_url("post"))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Event Loop")
        loop.close()
    