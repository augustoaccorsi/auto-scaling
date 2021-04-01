import os, subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from autoscaling import AutoScaling

auto_scaling_group = "os.environ['AUTO_SCALING_GROUP']"
region = "os.environ['REGION']"
env = 'dev'

def auto_scaling_check():
    print("Executing Analysis on Auto Scaling Group "+auto_scaling_group)
    autoscaling = AutoScaling(auto_scaling_group, region)
    autoscaling.create_files()
    autoscaling.read_cpu()
    print("Analysis Completed")

def auto_scaling_check_local():
    print("Executing Analysis on Auto Scaling Group "+"web-app-asg")
    autoscaling = AutoScaling("web-app-asg", "sa-east-1")
    autoscaling.create_files()
    autoscaling.read_cpu()
    print("Analysis Completed")

if __name__ == '__main__':
    if env == 'dev':    
        auto_scaling_check_local()
        scheduler = BlockingScheduler()
        scheduler.add_job(auto_scaling_check_local, 'interval', minutes=1)
        scheduler.start()
    else:
        auto_scaling_check()
        scheduler = BlockingScheduler()
        scheduler.add_job(auto_scaling_check, 'interval', minutes=1)
        scheduler.start()