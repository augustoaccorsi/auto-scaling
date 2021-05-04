from autoscalinggroup import Instance
from timeseries import Timeseries
import threading, queue, datetime
from openpyxl import load_workbook
from microservice import Microservice


class Autoscaling:
    def __init__(self, instances, autoScalingGroup, autoScalingClient):
        self._instances = instances
        self._auto_scaling_group = autoScalingGroup
        self._autoScalingClient = autoScalingClient
        self._terminated = [] 

        self._PROACTIVE_DIFF = 45
        self._ACCURACY = 70
        self._SCALE_UP = 70
        self._SCALE_DOWN = 30
        
        self._cooldown = False
    
    def scale_up(self, instancesUp):
        self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        print("Autoscaling Group scalled up, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        self._cooldown = True
        return True

    def scale_down(self, instancesDown):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
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

    def scale(self, microservice):
        if microservice._cpu_utilization >= self._SCALE_UP:
            total =  (microservice._cpu_total * 100) / ((len(microservice._instances)+1) * 100) 
            if total >= self._SCALE_UP:
                return self.scale_up(2)
            else:
                return self.scale_up(1)
        elif microservice._cpu_utilization <= self._SCALE_DOWN and len(microservice._instances) > 1:            
            try:
                total =  (microservice._cpu_total * 100) / ((len(microservice._instances)-1) * 100)
            except:
                total =  (microservice._cpu_total * 100) / ((len(microservice._instances)) * 100)

            if total <= self._SCALE_DOWN and len(microservice._instances) > 2:
                return self.scale_down(2)
            else:
                return self.scale_down(1)
        
        return True 

    def proactive_scale(self, microservice):
        return False
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
            cpu_count = 0
            netin_count = 0
            netout_count = 0

            for instance in microservice._instances:
                if abs(float(cpu._forecast[0])-float(microservice._cpu_total)) >= self._PROACTIVE_DIFF:
                    cpu_count +=1
                if abs(float(netin._forecast[0])-float(microservice._network_in)) >= self._PROACTIVE_DIFF:
                    netin_count +=1
                if abs(float(netout._forecast[0])-float(microservice._network_out)) >= self._PROACTIVE_DIFF:
                    netout_count +=1
            
            if float(cpu._accuracy) >= self._ACCURACY or float(netin._accuracy) >= self._ACCURACY or float(netout._accuracy) >= self._ACCURACY:
                if cpu_count > 0 or netin_count > 0 or netout_count > 0:
                    print("PROATIVO")
                    return self.scale(microservice)
        except Exception as e:
            print(e)

        print(str(now))

        return False

    def reactive_scale(self, microservice):
        return self.scale(microservice)

    def execute(self, microservice):        
        if not self.proactive_scale(microservice):
            return self.reactive_scale(microservice)
        else:
            return True