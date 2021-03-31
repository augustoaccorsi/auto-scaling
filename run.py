import os, subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from Autoscaling import AutoScaling

auto_scaling_group = os.environ['AUTO_SCALING_GROUP']
region = os.environ['REGION']
env = os.environ['ENV']

def auto_scaling_check():
    print("Executing Analysis on Auto Scaling Group "+auto_scaling_group)
    autoscaling = AutoScaling(auto_scaling_group, region)
    autoscaling.create_files()
    autoscaling.read_cpu()
    print("Analysis Completed")


if __name__ == '__main__':
    if env == 'dev':    
        autoscaling = AutoScaling("web-app-asg", "sa-east-1")
        autoscaling.create_files()
        autoscaling.read_cpu()
    else:
        auto_scaling_check()
        scheduler = BlockingScheduler()
        scheduler.add_job(auto_scaling_check, 'interval', minutes=1)
        scheduler.start()