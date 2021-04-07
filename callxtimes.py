import requests, sys
import datetime, timedelta

urlPost = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000/engine/mandelbrot?max_iter=1000&width=1000&height=1000"
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

