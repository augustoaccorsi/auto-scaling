import requests, sys

url = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000/engine/mandelbrot"
#url = "http://augusto-accorsi-engine-elb-206353658.sa-east-1.elb.amazonaws.com:5000"

for i in range(int(sys.argv[1])):
    res = requests.post(url) 
    #res = requests.get(url) 
    print("Call " + str(i+1) + " : " + str(res.status_code))    