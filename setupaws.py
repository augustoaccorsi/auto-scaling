import boto3

class AWS:
    def __initi__(self, region):
        self._region = region
        self._auto_scaling_group = boto3.client('autoscaling')


    def create_asg_launch_configuration(self):
        self._auto_scaling_group
