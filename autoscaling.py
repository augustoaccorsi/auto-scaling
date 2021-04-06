class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient

    def scale_up(self):
        self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + 1))
        print("Autoscaling Group scalled up, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() + 1)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() + 1))
    
    def scale_down(self):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - 1))
        print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - 1)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - 1))

    def reactive_scale(self, instance): # colocar mais uma métrica se possível
        if instance.getCpuUtilization() >= 70:
            instance.incrementTriggerUp()
            print("up trigger: "+str(instance.getTriggerUp()))
            if instance.getTriggerUp() == 3:
                self.scale_up()
                instance.clearTriggerUp()
                return True

        if instance.getCpuUtilization() <= 30 and len(self._instances) >= 2:
            instance.incrementTriggerDown()
            print("down trigger: "+str(instance.getTriggerDown()))
            if instance.getTriggerDown() == 3:
                self.scale_down()
                instance.clearTriggerDown()
                return True
    
    def proactive_scale(self):
        print("TODO")       

    def process(self):
        for instance in self._instances:
            if instance.getLifecycleState() == "InService":
              result = self.reactive_scale(instance)
              if result == True:
                  return result
        return result
