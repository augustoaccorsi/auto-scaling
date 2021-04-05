import os, subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from autoscaling import AutoScaling

auto_scaling_group = "os.environ['AUTO_SCALING_GROUP']"
region = "os.environ['REGION']"
accessKeyId = "os.environ['ACCESS_KEY']"
secretAccessKey = "os.environ['SECRET_KEY']"
sessionToken = "os.environ['SESSION_TOKEN']"
env = "dev" #os.environ['ENV']

class Run:
    def __init__(self):        
        #self._autoscaling = AutoScaling(auto_scaling_group, region, accessKeyId, secretAccessKey, sessionToken)   
        self._autoscaling = AutoScaling("engine-asg", "sa-east-1") 

    def auto_scaling_check(self):
        print("Executing Analysis on Auto Scaling Group "+auto_scaling_group)
        self._autoscaling.create_files()
        self._autoscaling.read_instances()
        print("Analysis Completed")
        print("----------------------------------")

    def auto_scaling_check_local(self):
        print("Executing Analysis on Auto Scaling Group "+"engine-asg")
        autoscaling = AutoScaling("engine-asg", "sa-east-1")
        autoscaling.create_files()
        autoscaling.read_instances()
        print("Analysis Completed")
        print("----------------------------------")

if __name__ == '__main__':
    run = Run()
    if env == 'dev':
        print("----------------------------------")   
        run.auto_scaling_check_local()
        scheduler = BlockingScheduler()
        scheduler.add_job(run.auto_scaling_check_local, 'interval', minutes=1)
        scheduler.start()
    else:
        print("----------------------------------")
        run.auto_scaling_check()
        scheduler = BlockingScheduler()
        scheduler.add_job(run.auto_scaling_check, 'interval', minutes=1)
        scheduler.start()