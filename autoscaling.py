from autoscalinggroup import Instance
from timeseries import Timeseries
import threading, queue, datetime
from openpyxl import load_workbook


class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self._terminated = [] 

        self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE = 3
        
        self._cooldown = False
        
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
        self._cooldown = True
        return True

    def scale_down(self, instancesDown):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            self.clearTriggerDown()
            self._cooldown = True
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

    def arima_call(self, dataset, output, next_forecast, queue):
        timeseries = Timeseries(dataset)
        timeseries.execute(output, next_forecast)
        print()
        queue.put(timeseries)

    def proactive_scale(self):
        # creating thread
        print("Start Forecasting")
        now = datetime.datetime.now()

        q1 = queue.Queue()
        q2 = queue.Queue()
        q3 = queue.Queue()

        t1 = threading.Thread(target=self.arima_call, args=('cpu', True, 10, q1))
        t2 = threading.Thread(target=self.arima_call, args=('netin', True, 10, q2))
        t3 = threading.Thread(target=self.arima_call, args=('netout', True, 10, q3))
    
        # starting thread
        t1.start()
        t2.start()
        t3.start()
    
        # wait until thread is completely executed
        t1.join()
        t2.join()
        t3.join() 
  
        cpu = (q1.get())
        netin = (q2.get())
        netout = (q3.get())
######################################
        workbook = load_workbook(filename = 'dataset\\all.xlsx')
        worksheet = workbook['Sheet1']
        
        worksheet.cell(column=9,row=worksheet.max_row, value=cpu._accuracy)
        worksheet.cell(column=10,row=worksheet.max_row, value=netin._accuracy)
        worksheet.cell(column=11,row=worksheet.max_row, value=netout._accuracy)

        workbook.save(filename = 'dataset\\all.xlsx')
        workbook.close()
######################################
        now = datetime.datetime.now() - now

        if cpu._accuracy > 70:
            count = 0
            for forecast in cpu._forecast:
                if forecast > 70:
                    count+=1
            
            if count >= 3:
                return False

        print(str(now))


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

        if self._cooldown == True:
            self

        if self.proactive_scale() == True:
            print("PROACTIVE ACTIVATED")
            #result = self.scale_up(1)

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