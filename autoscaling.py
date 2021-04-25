from autoscalinggroup import Instance
from timeseries import Timeseries

class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self._terminated = [] 

        self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE = 3
        
    def clearTriggerUp(self):
        for instance in self._instances:
            instance.clearTriggerUp()
    
    def clearTriggerDown(self):
        for instance in self._instances:
            instance.clearTriggerDown()

    def scale_up(self, instancesUp):
        self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        print("Autoscaling Group scalled up, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        self.clearTriggerUp()
        return True

    def scale_down(self, instancesDown):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            self.clearTriggerDown()
            return True

    def reactive_scale(self, instance): # colocar mais uma métrica se possível
        count = 0
        for inst in self._instances:
            if inst.getLifecycleState() == "Running" and inst.getHealthStatus() == "InService" and inst.getStatus() == "Passed":
                count+=1

        if instance.getCpuUtilization() >= 70:
            instance.incrementTriggerUp()
            print("["+instance.getInstanceId()+"] scale up trigger: "+str(instance.getTriggerUp()))
            return True
        elif instance.getCpuUtilization() <= 30 and count >= 2:
            instance.incrementTriggerDown()
            print("["+instance.getInstanceId()+"] scale down trigger: "+str(instance.getTriggerDown()))
            return True
        else:
            self.clearTriggerDown()
            self.clearTriggerUp()
        return False

    def proactive_scale(self):
        cpu_ts = Timeseries('cpu')
        netin_ts = Timeseries('netin')
        netout_ts = Timeseries('netout')
    
        cpu = cpu_ts.execute(True, 5)
        print()
        netin = netin_ts.execute(True, 5)
        print()
        netout = netout_ts.execute(True, 5)
        print()
        
        return False
    
    def process(self):

        reactive = False
        proactive = False
        result = False
        for instance in self._instances:
            if instance.getLifecycleState() == "Running" and instance.getHealthStatus() == "InService" and instance.getStatus() == "Passed":
              reactive = self.reactive_scale(instance)
        instancesDown = 0
        instancesUp = 0

        if self.proactive_scale() == True:
            print("TODO PROACTIVE")


        elif reactive == True:
            for instance in self._instances:
                if instance.getTriggerDown() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                    instancesDown +=1
                if instance.getTriggerUp() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                    instancesUp +=1

        if instancesDown > 0:
            if instancesDown == len(self._instances):
                result = self.scale_down(len(self._instances) - 1)
            else:
                result = self.scale_down(instancesDown)

        if instancesUp > 0:
            if instancesUp == 1:
                result = self.scale_up(1)
            else:
                result = self.scale_up(instancesUp)

        return result