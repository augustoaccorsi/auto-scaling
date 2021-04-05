class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self.process()
    
    def process(self):
        for instance in self._instances:
            print(instance)

    def scale_up(self):
        response = self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + 1))
        print(response)
    
    def scale_down(self):
        response = self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - 1))
        print(response)

    def reactive_scale(self, cpuUtilization):
        if float(cpuUtilization) >= 70:
            self.scale_up()
        if float(cpuUtilization) <= 20 and len(self._instances) >=2:
            self.scale_down()