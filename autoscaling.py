from time import time
from autoscalinggroup import Instance
from timeseries import Timeseries
import threading, queue, datetime
from openpyxl import load_workbook
from microservice import Microservice
import pandas as pd
import numpy as np
import statistics, math

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

        self._CPU_UPPER_TRESHOLD = None
        self._CPU_LOWER_TRESHOLD = None

        self._NETIN_UPPER_TRESHOLD = None
        self._NETIN_LOWER_TRESHOLD = None

        self._NETOUT_UPPER_TRESHOLD = None
        self._NETOUT_LOWER_TRESHOLD = None
        
        self._cooldown = False
        
        self.set_thresholds()
        
    def calculate_threasholds(self, values):

        
        upper =  np.percentile(np.sort(values), 90)
        lower = statistics.median(np.sort(values))

        #return math.modf(upper)[1], math.modf(lower)[1]

        return upper, lower

    def get_dataset_data(self, dataset):
        data_xls = pd.read_excel('dataset\\'+dataset+'.xlsx', 'Sheet1', dtype=str, index_col=None)
        data_xls.to_csv('dataset\\'+dataset+'.csv', encoding='utf-8', index=False) 
        df=pd.read_csv('dataset\\'+dataset+'.csv')

        date, value = df.date.to_list(), df.value.to_list()
        
        try:
            last_read = datetime.datetime.strptime(date[len(date)-1], '%m/%d/%Y %H:%M:%S')
        except:
            last_read = datetime.datetime.strptime(date[len(date)-1], '%m/%d/%Y %H:%M')

        values = []

        for i in reversed(range(len(value))):
            
            try:
                aux = (last_read - datetime.datetime.strptime(date[i], '%m/%d/%Y %H:%M:%S')).total_seconds()
            except:
                aux = (last_read - datetime.datetime.strptime(date[i], '%m/%d/%Y %H:%M')).total_seconds()
            
            if aux <= 3600:
                values.append(value[i])
        
        return self.calculate_threasholds(values) 

    def set_thresholds(self):
        self._CPU_UPPER_TRESHOLD, self._CPU_LOWER_TRESHOLD = self.get_dataset_data('cpu')
        self._NETIN_UPPER_TRESHOLD, self._NETIN_LOWER_TRESHOLD =  self.get_dataset_data('netin')
        self._NETOUT_UPPER_TRESHOLD, self._NETOUT_LOWER_TRESHOLD = self.get_dataset_data('netout')

        print("CPU: "+str(self._CPU_UPPER_TRESHOLD)+" / "+str(self._CPU_LOWER_TRESHOLD))
        print("IN:  "+str(self._NETIN_UPPER_TRESHOLD)+" / "+str(self._NETIN_LOWER_TRESHOLD))
        print("OUT: "+str(self._NETOUT_UPPER_TRESHOLD)+" / "+str(self._NETOUT_LOWER_TRESHOLD))
    
    def scale_up(self, instancesUp):
        #self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        print("Autoscaling Group scalled up, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() + instancesUp))
        #self._cooldown = True
        return True

    def scale_down(self, instancesDown):
        if self._auto_scaling_group.getDesiredCapacity() > 1:
            #self._autoScalingClient.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - instancesDown))
            #self._cooldown = True
            return True

    def arima_call(self, dataset, output, next_forecast, queue):
        timeseries = Timeseries(dataset)
        timeseries.execute(output, next_forecast)
        print()
        queue.put(timeseries)
    
    def update_file(self, scale):        
        workbook = load_workbook(filename = 'dataset\\all.xlsx')
        worksheet = workbook['Sheet1']
        worksheet.cell(column=5,row=worksheet.max_row, value=scale)
        workbook.save(filename = 'dataset\\all.xlsx')
        workbook.close()

    def save_file(self, cpu, netin, netout):
        workbook = load_workbook(filename = 'dataset\\all.xlsx')
        worksheet = workbook['Sheet1']        
        
        worksheet.cell(column=7,row=worksheet.max_row, value=str(self._CPU_UPPER_TRESHOLD))        
        worksheet.cell(column=8,row=worksheet.max_row, value=str(self._CPU_LOWER_TRESHOLD))        
        worksheet.cell(column=9,row=worksheet.max_row, value=str(self._NETIN_UPPER_TRESHOLD))       
        worksheet.cell(column=10,row=worksheet.max_row, value=str(self._NETIN_LOWER_TRESHOLD))        
        worksheet.cell(column=11,row=worksheet.max_row, value=str(self._NETOUT_UPPER_TRESHOLD))        
        worksheet.cell(column=12,row=worksheet.max_row, value=str(self._NETOUT_LOWER_TRESHOLD))

        worksheet.cell(column=13,row=worksheet.max_row, value=cpu._arima_order)
        try:
            worksheet.cell(column=14,row=worksheet.max_row, value=str(cpu._forecast[0]))
            worksheet.cell(column=15,row=worksheet.max_row, value=str(cpu._forecast[1]))
            worksheet.cell(column=16,row=worksheet.max_row, value=str(cpu._forecast[2]))
        except:
            worksheet.cell(column=14,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=15,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=16,row=worksheet.max_row, value=str(0))
        worksheet.cell(column=17,row=worksheet.max_row, value=netin._accuracy)
        worksheet.cell(column=18,row=worksheet.max_row, value=netin._arima_order)
        try:
            worksheet.cell(column=19,row=worksheet.max_row, value=str(netin._forecast[0]))
            worksheet.cell(column=20,row=worksheet.max_row, value=str(netin._forecast[1]))
            worksheet.cell(column=21,row=worksheet.max_row, value=str(netin._forecast[2]))
        except:
            worksheet.cell(column=19,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=20,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=21,row=worksheet.max_row, value=str(0))
        worksheet.cell(column=22,row=worksheet.max_row, value=netout._accuracy)
        worksheet.cell(column=23,row=worksheet.max_row, value=netout._arima_order)
        try:
            worksheet.cell(column=24,row=worksheet.max_row, value=str(netout._forecast[0]))
            worksheet.cell(column=25,row=worksheet.max_row, value=str(netout._forecast[1]))
            worksheet.cell(column=26,row=worksheet.max_row, value=str(netout._forecast[2]))
        except:
            worksheet.cell(column=24,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=25,row=worksheet.max_row, value=str(0))
            worksheet.cell(column=26,row=worksheet.max_row, value=str(0))

        workbook.save(filename = 'dataset\\all.xlsx')
        workbook.close()

    def scale(self, microservice):
        if microservice._cpu_utilization >= self._SCALE_UP:
            total =  (microservice._cpu_total * 100) / ((microservice._count+1) * 100) 
            if total >= self._SCALE_UP:
                self.update_file(1)
                return self.scale_up(2)
            else:
                self.update_file(1)
                return self.scale_up(1)
        elif microservice._cpu_utilization <= self._SCALE_DOWN and microservice._count > 1:            
            try:
                total =  (microservice._cpu_total * 100) / ((microservice._count-1) * 100)
            except:
                total =  (microservice._cpu_total * 100) / ((microservice._count) * 100)

            if total <= self._SCALE_DOWN and microservice._count > 2:
                self.update_file(2)
                return self.scale_down(2)
            else:
                self.update_file(2)
                return self.scale_down(1)
        
        return False

    def compare_proactive(self, value1, value2):
        if value1 > value2:
            return True
        return False
    
    def scale_v2(self, microservice, proactive):
        if proactive == True:
            if (microservice._cpu_utilization > self._CPU_UPPER_TRESHOLD and microservice._cpu_accuracy >= self._ACCURACY) or (microservice._network_in > self._NETIN_UPPER_TRESHOLD and microservice._network_in_accuracy >= self._ACCURACY) or (microservice._network_out > self._NETOUT_UPPER_TRESHOLD and microservice._network_out_accuracy >= self._ACCURACY):
                total =  (microservice._cpu_total * 100) / ((microservice._count+1) * 100) 
                if total >= self._CPU_UPPER_TRESHOLD:
                    self.update_file("pro up")
                    print("PROATIVO")
                    return self.scale_up(2)
                else:
                    self.update_file("pro up")
                    print("PROATIVO")
                    return self.scale_up(1)
            elif microservice._count > 1 and (microservice._cpu_utilization > self._CPU_UPPER_TRESHOLD and microservice._cpu_accuracy >= self._ACCURACY) or (microservice._network_in > self._NETIN_UPPER_TRESHOLD and microservice._network_in_accuracy >= self._ACCURACY) or (microservice._network_out > self._NETOUT_UPPER_TRESHOLD and microservice._network_out_accuracy >= self._ACCURACY):      
                try:
                    total =  (microservice._cpu_total * 100) / ((microservice._count-1) * 100)
                except:
                    total =  (microservice._cpu_total * 100) / ((microservice._count) * 100)

                if total <= self._CPU_LOWER_TRESHOLD and microservice._count > 2:
                    self.update_file(2)
                    print("PROATIVO")
                    self.update_file("pro down")
                else:
                    self.update_file(2)
                    print("PROATIVO")
                    self.update_file("pro down")
        else:
            if microservice._cpu_utilization > self._CPU_UPPER_TRESHOLD or microservice._network_in > self._NETIN_UPPER_TRESHOLD or microservice._network_out > self._NETOUT_UPPER_TRESHOLD:
                total =  (microservice._cpu_total * 100) / ((microservice._count+1) * 100)
                if total >= self._CPU_UPPER_TRESHOLD:
                    self.update_file("rea up")
                    print("REATIVO")
                    return self.scale_up(2)
                else:
                    self.update_file("rea up")
                    print("REATIVO")
                    return self.scale_up(1)
            elif microservice._count > 1 and (microservice._cpu_utilization < self._CPU_LOWER_TRESHOLD or microservice._network_in < self._NETIN_LOWER_TRESHOLD or microservice._network_out < self._NETOUT_LOWER_TRESHOLD):      
                try:
                    total =  (microservice._cpu_total * 100) / ((microservice._count-1) * 100)
                except:
                    total =  (microservice._cpu_total * 100) / ((microservice._count) * 100)

                if total <= self._CPU_LOWER_TRESHOLD and microservice._count > 2:
                    self.update_file("rea down")
                    print("REATIVO")
                    return self.scale_down(2)
                else:
                    self.update_file("rea down")
                    print("REATIVO")
                    return self.scale_down(1)
        
        return False 

    def arima(self):
        q1 = queue.Queue()
        q2 = queue.Queue()
        q3 = queue.Queue()

        t1 = threading.Thread(target=self.arima_call, args=('cpu', True, 3, q1))
        t2 = threading.Thread(target=self.arima_call, args=('netin', True, 3, q2))
        t3 = threading.Thread(target=self.arima_call, args=('netout', True, 3, q3))
    
        # starting thread
        t1.start()
        t2.start()
        t3.start()
    
        # wait until thread is completely executed
        t1.join()
        t2.join()
        t3.join() 
  
        return q1.get(), q2.get(), q3.get()

    def proactive_scale(self, microservice):
        # creating thread
        print("Start Forecasting")

        now = datetime.datetime.now()

        cpu, netin, netout = self.arima()

        now = datetime.datetime.now() - now

        self.save_file(cpu, netin, netout)

        try:
            microservice._cpu_utilization = cpu._forecast[0]
        except:
            pass
        try:
            microservice._network_in = netin._forecast[0]
        except:
            pass
        try:
            microservice._network_out = netout._forecast[0]
        except:
            pass

        microservice._cpu_accuracy = cpu._accuracy
        microservice._network_in_accuracy = netin._accuracy
        microservice._network_out_accuracy = netout._accuracy
        
        #return self.scale(microservice)
        return self.scale_v2(microservice, True)

        #se precisão de cpu e rede forem >= a 70% eo valor atual não for praticamente ZERO				
	        #se o próximo valor é maior que antigo			
		        #se o próximo valor for muito maior que o antigo		
			        #aumenta uma instnacia	
				        #cooldown de quatro lidas
        '''
        try:
            cpu_count = 0
            netin_count = 0
            netout_count = 0

            # crescimento de CPU é diretamente proporcional ao crescimento de Rede




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
        '''
        print(str(now))

        return False

    def reactive_scale(self, microservice):
        #if not self.scale(microservice):
        if not self.scale_v2(microservice, False):
            self.update_file(0)
            return False
        return True

    def execute(self, microservice):
        if not self.proactive_scale(microservice):
            return self.reactive_scale(microservice)
        else:
            return True