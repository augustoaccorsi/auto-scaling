from autoscalinggroup import Instance
from timeseries import Timeseries
import threading, queue, datetime
from openpyxl import load_workbook


class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient, cpu, netin, netout):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self._terminated = [] 

        self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE = 1
        self._PROACTIVE_DIFF = 45
        self._ACCURACY = 70
        self._SCALE_UP = 70
        self._SCALE_DOWN = 30
        
        self._cooldown = False

        try:
            self._cpu = float(cpu)
        except:
            pass
        try:
            self._netin = float(netin)
        except:
            pass
        try:
            self._netout = float(netout)
        except:
            pass

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

    def arima_call(self, dataset, output, next_forecast, queue):
        timeseries = Timeseries(dataset)
        timeseries.execute(output, next_forecast)
        print()
        queue.put(timeseries)
    
    def save_file(self, cpu, netin, netout):
        workbook = load_workbook(filename = 'dataset\\all.xlsx')
        worksheet = workbook['Sheet1']
        
        worksheet.cell(column=9,row=worksheet.max_row, value=cpu._accuracy)
        worksheet.cell(column=10,row=worksheet.max_row, value=cpu._arima_order)
        try:
            worksheet.cell(column=11,row=worksheet.max_row, value=str(cpu._forecast[0]))
            worksheet.cell(column=12,row=worksheet.max_row, value=str(cpu._forecast[1]))
            worksheet.cell(column=13,row=worksheet.max_row, value=str(cpu._forecast[2]))
        except:
            worksheet.cell(column=11,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=12,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=13,row=worksheet.max_row, value=str(0))
        worksheet.cell(column=14,row=worksheet.max_row, value=netin._accuracy)
        worksheet.cell(column=15,row=worksheet.max_row, value=netin._arima_order)
        try:
            worksheet.cell(column=16,row=worksheet.max_row, value=str(netin._forecast[0]))
            worksheet.cell(column=17,row=worksheet.max_row, value=str(netin._forecast[1]))
            worksheet.cell(column=18,row=worksheet.max_row, value=str(netin._forecast[2]))
        except:
            worksheet.cell(column=16,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=17,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=18,row=worksheet.max_row, value=str(0))
        worksheet.cell(column=19,row=worksheet.max_row, value=netout._accuracy)
        worksheet.cell(column=20,row=worksheet.max_row, value=netout._arima_order)
        try:
            worksheet.cell(column=21,row=worksheet.max_row, value=str(netout._forecast[0]))
            worksheet.cell(column=22,row=worksheet.max_row, value=str(netout._forecast[1]))
            worksheet.cell(column=23,row=worksheet.max_row, value=str(netout._forecast[2]))
        except:
            worksheet.cell(column=21,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=22,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=23,row=worksheet.max_row, value=str(0))

        workbook.save(filename = 'dataset\\all.xlsx')
        workbook.close()
    '''
    def create_threads(self, dataset, output, forcast):
        queue = queue.Queue()
        return threading.Thread(target=self.arima_call, args=(dataset, output, forecast, queue))
    '''
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
        now = datetime.datetime.now() - now

        self.save_file(cpu, netin, netout)

        #se precisão de cpu e rede forem >= a 70% eo valor atual não for praticamente ZERO				
	        #se o próximo valor é maior que antigo			
		        #se o próximo valor for muito maior que o antigo		
			        #aumenta uma instnacia	
				        #cooldown de quatro lidas

        try:
            print(abs(float(cpu._forecast[0])-self._cpu))
            print(abs(float(netin._forecast[0])-self._netin))
            print(abs(float(netout._forecast[0])-self._netout))

            cpu_count = 0
            netin_count = 0
            netout_count = 0
            total_cpu = 0
            netout_total = 0
            netin_total = 0

            for instance in self._instances:
                total_cpu = total_cpu + float(instance.getCpuUtilization())
                netout_total = netout_total + float(instance.getNetworkOut())
                netin_total = netin_total + float(instance.getNetworkIn())
                
                '''
                if abs(float(cpu._forecast[0])-float(instance.getCpuUtilization())) >= self._PROACTIVE_DIFF:
                    cpu_count +=1
                if abs(float(netin._forecast[0])-float(instance.getNetworkIn())) >= self._PROACTIVE_DIFF:
                    netin_count +=1
                if abs(float(netout._forecast[0])-float(instance.getNetworkOut())) >= self._PROACTIVE_DIFF:
                    netout_count +=1
                '''
                if abs(float(cpu._forecast[0])-float(total_cpu)) >= self._PROACTIVE_DIFF:
                    cpu_count +=1
                if abs(float(netin._forecast[0])-float(netin_total)) >= self._PROACTIVE_DIFF:
                    netin_count +=1
                if abs(float(netout._forecast[0])-float(netout_total)) >= self._PROACTIVE_DIFF:
                    netout_count +=1

            '''
            Instance 1:  i-00d756bd3a4bc1a80
            Lifecycle State: Running - InService - Passed
            CPU Usage: 66.5%
            Network In: 18.412Kb
            Network Out: 100.868Kb

            Instance 2:  i-0a4b6291d30ad31b3
            Lifecycle State: Running - InService - Passed
            CPU Usage: 31.9672%
            Network In: 13.842Kb
            Network Out: 11.604Kb
            '''
            
            if float(cpu._accuracy) >= self._ACCURACY or float(netin._accuracy) >= self._ACCURACY or float(netout._accuracy) >= self._ACCURACY:
                if cpu_count > 0 or netin_count > 0 or netout_count > 0:
                    '''
                    if len(self._instances) == 1:
                        print("tem que subir")
                        return self.scale_up(1)
                    else:
                    '''

                    utiliztion = (total_cpu * 100) / (len(self._instances) * 100)

                    print(utiliztion)

                    if utiliztion >= self._SCALE_UP:
                        print("pro up")
                        total =  (total_cpu * 100) / ((len(self._instances)+1) * 100) 
                        if total >= self._SCALE_UP:
                            print("pro up2")
                            return self.scale_up(2)
                        else:
                            print("pro up1")
                            return self.scale_up(1)
                    elif utiliztion <= self._SCALE_DOWN: 
                        print("pro down")
                        
                        try:
                            total =  (total_cpu * 100) / ((len(self._instances)-1) * 100)
                        except:
                            total =  (total_cpu * 100) / ((len(self._instances)) * 100)

                        if total <= self._SCALE_DOWN and len(self._instances) > 2:
                            print("pro down2")
                            return self.scale_down(2)
                        else:
                            print("pro down1")
                            return self.scale_down(1)

                    return True
            # 0 -> 7    NOT
                # 15 -> 40  YES
        except Exception as e:
            print(e)

        print(str(now))

        return False

    def reactive_scale(self):
        count = 0
        for instance in self._instances:
            if instance.getLifecycleState() == "Running" and instance.getHealthStatus() == "InService" and instance.getStatus() == "Passed":
                count +=1

        reactive_trigger = False
        instancesDown = 0
        instancesUp = 0

        for instance in self._instances:
            if instance.getCpuUtilization() >= self._SCALE_UP:
                instance.incrementTriggerUp()
                print("["+instance.getInstanceId()+"] scale up trigger: "+str(instance.getTriggerUp()))
                reactive_trigger = True
            elif instance.getCpuUtilization() <= self._SCALE_DOWN and count >= 2:
                instance.incrementTriggerDown()
                print("["+instance.getInstanceId()+"] scale down trigger: "+str(instance.getTriggerDown()))
                reactive_trigger = True
            else:
                self.clearTriggerDown()
                self.clearTriggerUp()
            
        if reactive_trigger == True:
                for instance in self._instances:
                    if instance.getTriggerDown() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                        instancesDown +=1
                        pass
                    if instance.getTriggerUp() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                        instancesUp +=1

        if instancesDown > 0:
            if instancesDown == len(self._instances):
                return self.scale_down(len(self._instances) - 1)
            else:
                return self.scale_down(instancesDown)

        if instancesUp > 0:
            if instancesUp == 1:
                return self.scale_up(1)
            else:
                return self.scale_up(instancesUp)


    def reactive2(self, instance): # colocar mais uma métrica se possível
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
    
    def execute(self):        
        if not self.proactive_scale():
            return self.reactive_scale()
        else:
            return True

        '''
        if not self.proactive_scale():            
            for instance in self._instances:
                if instance.getLifecycleState() == "Running" and instance.getHealthStatus() == "InService" and instance.getStatus() == "Passed":
                    reactive = self.reactive_scale(instance)

            if reactive == True:
                for instance in self._instances:
                    if instance.getTriggerDown() == self._NUMBER_OF_CHECKS_TO_REATIVE_SCALE:
                        instancesDown +=1
                        pass
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
            '''
        #return result