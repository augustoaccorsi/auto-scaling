import datetime, timedelta
from autoscalinggroup import Instance

class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self._terminated = [] 

        self._up = False

        self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE = 3

    def setTerminatedInstances(self, instancesDown):
       # self._oldest = self._oldest - datetime.timedelta(days=7300) #dominuindo dez anos para não ter problema com instancias muito antigas
        launchTime = []
        for instance in self._instances:
            launchTime.append(instance.getLaunchTime())
        oldestLaunchedTime = []
        
        for i in range(instancesDown):
            oldestLaunchedTime.append(min(launchTime))
            launchTime.remove(min(launchTime))
        
        for instance in self._instances:
           if instance.getLaunchTime() in oldestLaunchedTime:
               self._terminated.append(instance.getInstanceId())

        print(self._terminated)
        
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
        self._up = True
        return True

    def scale_down(self, instancesDown):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            self.clearTriggerDown()
            self.setTerminatedInstances(instancesDown)
            return True

    def reactive_scale(self, instance): # colocar mais uma métrica se possível
        if instance.getCpuUtilization() >= 70:
            instance.incrementTriggerUp()
            print("["+instance.getInstanceId()+"] scale up trigger: "+str(instance.getTriggerUp()))
            return True

        count = 0
        for inst in self._instances:
            if inst.getLifecycleState() == "Running" and inst.getStatus() == "Passed":
                count+=1

        if instance.getCpuUtilization() <= 30 and count >= 2:
            instance.incrementTriggerDown()
            print("["+instance.getInstanceId()+"] scale down trigger: "+str(instance.getTriggerDown()))
            return True

        return False

    def proactive_scale(self, instance):
        return False

    def process(self):

        reactive = False
        proactive = False
        result = False
        for instance in self._instances:
            if instance.getLifecycleState() == "Running" and instance.getStatus() == "Passed":
              reactive = self.reactive_scale(instance)
              proactive = self.proactive_scale(instance)
        instancesDown = 0
        instancesUp = 0

        if proactive == True:
            print("TODO PROACTIVE")
        elif reactive == True:
            for instance in self._instances:
                if instance.getTriggerDown() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                    instancesDown +=1
                if instance.getTriggerUp() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                    print("hehe")
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
        

