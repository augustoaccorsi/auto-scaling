import json, os, xlsxwriter, datetime, timedelta, boto3, sys
from openpyxl import load_workbook
from autoscalinggroup import AutoScalingGroup, Instance, AvailabilityZone, LoadBalancer, EnabledMetric, Tags
from autoscaling import Autoscaling
import weakref

class App():
    _alive = []
    #def __init__(self, autoscalinggroup, region, accessKeyId, secretAccessKey, sessionToken):
    def __new__(self, autoscalinggroup, region):
        
        self = super().__new__(self)
        App._alive.append(self)

        self._autoscalinggroup = autoscalinggroup
        self._asg = boto3.client('autoscaling', region_name=region)
        self._cloud_watch = boto3.client('cloudwatch',  region_name=region)
        self._ec2 = boto3.client('ec2', region_name=region)
        self._elb = boto3.client('elb', region_name=region)

        self._region = region

        self._up = False

        self.lb_instnaces = []
        self._lb_name = ""

        #self._asg = boto3.client('autoscaling', region_name=region, aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey, aws_session_token=sessionToken)
        #self._cloud_watch = boto3.client('cloudwatch',  region_name=region, aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey, aws_session_token=sessionToken)

        self._auto_scaling_info = dict()
        self._auto_scaling_group = AutoScalingGroup()
        self._instances = []
        self._instances_ids = dict()
        
        self._cooldown = False
        self._cooldown_trigger = 0

        self.describe()
        
        return weakref.proxy(self)
    
    def commit_suicide(self):
        self._alive.remove(self)
    
    def renew_connection(self):
        self._asg = boto3.client('autoscaling', region_name=self._region)
        self._cloud_watch = boto3.client('cloudwatch',  region_name=self._region)
        self._ec2 = boto3.client('ec2',  region_name=self._region)

    def clear_all(self):
        self._auto_scaling_info = dict()
        self._auto_scaling_group = AutoScalingGroup()
        #self._instances = []
        #self._instances_ids = dict()

    def describe(self):
        
        if len(self._instances) > 0:
            self.clear_all()
            self.renew_connection()
        
        self._auto_scaling_info = self._asg.describe_auto_scaling_groups(AutoScalingGroupNames=[self._autoscalinggroup])
        self.build_auto_scaling_group()
        return self
        
    def build_availability_zones(self, availabilityZones):
        availabilityZoneList = []
        for zone in availabilityZones:
            avZone = AvailabilityZone()
            avZone.setAvailabilityZone(zone)
            availabilityZoneList.append(avZone)

        return availabilityZoneList
    
    def build_load_balancers(self, loadBalancers):
        loadBalancersList = []
        for lb in loadBalancers:
            ldb = LoadBalancer()
            ldb.setLoadBalancer(lb)
            loadBalancersList.append(ldb)
            loadBalancer = (self._elb.describe_load_balancers(LoadBalancerNames=[lb]))

            if not loadBalancer['LoadBalancerDescriptions'][0]['Instances'] in self._instances:
                self._instances_ids = (loadBalancer['LoadBalancerDescriptions'][0]['Instances'])
                self._auto_scaling_group.appendInstanceId((loadBalancer['LoadBalancerDescriptions'][0]['Instances']))
                self._lb_name = (loadBalancer['LoadBalancerDescriptions'][0]['LoadBalancerName'])
            
        return loadBalancersList
    
    def build_instances(self, instances):
        
        instancesList = []
        for instance in self._instances_ids:      

            if instance['InstanceId'] not in self.lb_instnaces:
                
                self.lb_instnaces.append(instance['InstanceId'])

                inst = Instance()
                inst.setInstanceId(instance['InstanceId'])

                state = self._ec2.describe_instances(InstanceIds=[instance['InstanceId']])
                inst.setLifecycleState(state['Reservations'][0]['Instances'][0]['State']['Name'].title())
                inst.setLaunchTime(state['Reservations'][0]['Instances'][0]['LaunchTime'])

                health = self._elb.describe_instance_health(LoadBalancerName=self._lb_name, Instances=[{'InstanceId': instance['InstanceId']}])
                inst.setHealthStatus(health['InstanceStates'][0]['State'])

                try:
                    status = self._ec2.describe_instance_status(InstanceIds=[instance['InstanceId']])
                    inst.setStatus(status['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status'].title())
                except:
                    inst.setStatus("-")

                instancesList.append(inst)
                self._instances.append(inst)

        self.update_instances()

        return self._instances

    def update_instances(self):
        for instance in self._instances:
            
            state = self._ec2.describe_instances(InstanceIds=[instance.getInstanceId()])
            instance.setLifecycleState(state['Reservations'][0]['Instances'][0]['State']['Name'].title())
            instance.setLaunchTime(state['Reservations'][0]['Instances'][0]['LaunchTime'])

            health = self._elb.describe_instance_health(LoadBalancerName=self._lb_name, Instances=[{'InstanceId': instance.getInstanceId()}])
            instance.setHealthStatus(health['InstanceStates'][0]['State'])

            try:
                status = self._ec2.describe_instance_status(InstanceIds=instance.getInstanceId())
                instance.setStatus(status['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status'].title())
            except:
                instance.setStatus("-")
        return self._instances

    def biuld_metrics(self, metrics):
        metricsList = []
        for metric in metrics:
            met = EnabledMetric()
            met.setEnabledMetric(metric['Metric'])
            met.setGranularity(metric['Granularity'])

        return metricsList
    
    def build_tags(self, tags):
        tagsList = []
        for tag in tags:
            tg = Tags()
            tg.setResourceId(tag['ResourceId'])
            tg.setResourceType(tag['ResourceType'])
            tg.setKey(tag['Key'])
            tg.setValue(tag['Value'])
            tg.setPropagateAtLaunch(tag['PropagateAtLaunch'])
        
        return tagsList

    def build_auto_scaling_group(self):
        self._auto_scaling_group.setAutoScalingGroupName(self._auto_scaling_info['AutoScalingGroups'][0]['AutoScalingGroupName'])
        self._auto_scaling_group.setAutoScalingGroupARN(self._auto_scaling_info['AutoScalingGroups'][0]['AutoScalingGroupARN'])
        self._auto_scaling_group.setLaunchConfigurationName(self._auto_scaling_info['AutoScalingGroups'][0]['LaunchConfigurationName'])
        self._auto_scaling_group.setMinSize(self._auto_scaling_info['AutoScalingGroups'][0]['MinSize'])
        self._auto_scaling_group.setMinSize(self._auto_scaling_info['AutoScalingGroups'][0]['MaxSize'])
        self._auto_scaling_group.setDesiredCapacity(self._auto_scaling_info['AutoScalingGroups'][0]['DesiredCapacity'])
        self._auto_scaling_group.setDefaultCooldown(self._auto_scaling_info['AutoScalingGroups'][0]['DefaultCooldown'])
        self._auto_scaling_group.setAvailabilityZones(self.build_availability_zones(self._auto_scaling_info['AutoScalingGroups'][0]['AvailabilityZones']))
        self._auto_scaling_group.setLoadBalancerNames(self.build_load_balancers(self._auto_scaling_info['AutoScalingGroups'][0]['LoadBalancerNames']))
        self._auto_scaling_group.setTargetGroupARNs(self._auto_scaling_info['AutoScalingGroups'][0]['TargetGroupARNs'])
        self._auto_scaling_group.setHealthCheckType(self._auto_scaling_info['AutoScalingGroups'][0]['HealthCheckType'])
        self._auto_scaling_group.setHealthCheckGracePeriod(self._auto_scaling_info['AutoScalingGroups'][0]['HealthCheckGracePeriod'])
        self._auto_scaling_group.setInstances(self.build_instances(self._auto_scaling_info['AutoScalingGroups'][0]['Instances']))
        self._auto_scaling_group.setCreatedTime(self._auto_scaling_info['AutoScalingGroups'][0]['CreatedTime'])
        self._auto_scaling_group.setSuspendedProcesses(self._auto_scaling_info['AutoScalingGroups'][0]['SuspendedProcesses'])
        self._auto_scaling_group.setVpcZoneIdentifier(self._auto_scaling_info['AutoScalingGroups'][0]['VPCZoneIdentifier'])
        self._auto_scaling_group.setEnabledMetrics(self.biuld_metrics(self._auto_scaling_info['AutoScalingGroups'][0]['EnabledMetrics']))
        self._auto_scaling_group.setTags(self.build_tags(self._auto_scaling_info['AutoScalingGroups'][0]['Tags']))
        self._auto_scaling_group.setTerminationPolicies(self._auto_scaling_info['AutoScalingGroups'][0]['TerminationPolicies'])
        self._auto_scaling_group.setNewInstancesProtectedFromScaleIn(self._auto_scaling_info['AutoScalingGroups'][0]['NewInstancesProtectedFromScaleIn'])
        self._auto_scaling_group.setServiceLinkedRoleARN(self._auto_scaling_info['AutoScalingGroups'][0]['ServiceLinkedRoleARN'])

        self.create_files()

    def create_files(self):
        if not os.path.isfile('dataset\\cpu.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\cpu.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'value')
            workbook.close()

        if not os.path.isfile('dataset\\netin.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\netin.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'value')
            workbook.close()

        if not os.path.isfile('dataset\\netout.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\netout.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'value')
            workbook.close()

        if not os.path.isfile('dataset\\packetin.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\packetin.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'value')
            workbook.close()

        if not os.path.isfile('dataset\\packetout.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\packetout.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'value')
            workbook.close()
        
        if not os.path.isfile('dataset\\all.xlsx'):
            workbook = xlsxwriter.Workbook('dataset\\all.xlsx')
            worksheet = workbook.add_worksheet()
            format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            worksheet.write('A1', 'date', format)
            worksheet.write('B1', 'cpu')
            worksheet.write('C1', 'netin')
            worksheet.write('D1', 'netout')
            worksheet.write('E1', 'packin')
            worksheet.write('F1', 'packout')
            worksheet.write('G1', 'instance')
            worksheet.write('H1', 'status')
            worksheet.write('I1', 'cpu_acc')
            worksheet.write('J1', 'cpu_model')
            worksheet.write('K1', 'cpu_pred1')
            worksheet.write('L1', 'cpu_pred2')
            worksheet.write('M1', 'cpu_pred3')
            worksheet.write('N1', 'netin_acc')
            worksheet.write('O1', 'netin_model')
            worksheet.write('P1', 'netin_pred1')
            worksheet.write('Q1', 'netin_pred2')
            worksheet.write('R1', 'netin_pred3')
            worksheet.write('S1', 'netout_acc')
            worksheet.write('T1', 'netout_model')
            worksheet.write('U1', 'netout_pred1')
            worksheet.write('V1', 'netout_pred2')
            worksheet.write('W1', 'netout_pred3')
            workbook.close()

    def save_into_file(self, datetime, cpu, netin, netout, packetin, packetout, lifecycleState, instance):
        workbook = load_workbook(filename = 'dataset\\cpu.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if cpu != None:
            worksheet.cell(column=2,row=newRowLocation, value=cpu)

        workbook.save(filename = 'dataset\\cpu.xlsx')
        workbook.close()

        workbook = load_workbook(filename = 'dataset\\netin.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if netin != None:
            worksheet.cell(column=2,row=newRowLocation, value=netin)

        workbook.save(filename = 'dataset\\netin.xlsx')
        workbook.close()

        workbook = load_workbook(filename = 'dataset\\netout.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if netout != None:
            worksheet.cell(column=2,row=newRowLocation, value=netout)

        workbook.save(filename = 'dataset\\netout.xlsx')
        workbook.close()

        workbook = load_workbook(filename = 'dataset\\packetin.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if packetin != None:
            worksheet.cell(column=2,row=newRowLocation, value=packetin)

        workbook.save(filename = 'dataset\\packetin.xlsx')
        workbook.close()

        workbook = load_workbook(filename = 'dataset\\packetout.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if packetout != None:
            worksheet.cell(column=2,row=newRowLocation, value=packetout)

        workbook.save(filename = 'dataset\\packetout.xlsx')
        workbook.close()

        workbook = load_workbook(filename = 'dataset\\all.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=datetime)
        if cpu != None:
            worksheet.cell(column=2,row=newRowLocation, value=cpu)
        if netin != None:
            worksheet.cell(column=3,row=newRowLocation, value=netin)
        if netout != None:
            worksheet.cell(column=4,row=newRowLocation, value=netout)
        if packetin != None:
            worksheet.cell(column=5,row=newRowLocation, value=packetin)
        if packetout != None:
            worksheet.cell(column=6,row=newRowLocation, value=packetout)
        worksheet.cell(column=7,row=newRowLocation, value=instance)
        worksheet.cell(column=8,row=newRowLocation, value=lifecycleState)

        workbook.save(filename = 'dataset\\all.xlsx')
        workbook.close()

    def get_metric(self, metric, instance, start_time, end_time, statistics):
        return self._cloud_watch.get_metric_statistics(Namespace='AWS/EC2',
            MetricName=metric,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance
                },
            ], StartTime=start_time, EndTime=end_time, Period=120, Statistics=[statistics]) 

    def read_instances(self):
        count = 0
        for instance in self._instances:

            if instance.getLifecycleState() == "Terminated":
                self._instances.remove(instance)
                break
            else:

                count+=1
                end_time = datetime.datetime.utcnow()
                
                start_time = end_time - datetime.timedelta(seconds=120) #buscar dados dos ultimos 2 minutos

                start_time = start_time.strftime('%m/%d/%Y %H:%M:%S')
                end_time = end_time.strftime('%m/%d/%Y %H:%M:%S')
            
                cpu =  self.get_metric("CPUUtilization", instance.getInstanceId(), start_time, end_time, "Maximum")
                networkIn =  self.get_metric("NetworkIn", instance.getInstanceId(), start_time, end_time, "Maximum")
                networkOut =  self.get_metric("NetworkOut", instance.getInstanceId(), start_time, end_time, "Maximum")
                networkPacketsIn =  self.get_metric("NetworkPacketsIn", instance.getInstanceId(), start_time, end_time, "Average")
                networkPacketsOut =  self.get_metric("NetworkPacketsOut", instance.getInstanceId(), start_time, end_time, "Average")
                        
                state = self._ec2.describe_instances(InstanceIds=[instance.getInstanceId()])
                instance.setLifecycleState(state['Reservations'][0]['Instances'][0]['State']['Name'].title())
                instance.setLaunchTime(state['Reservations'][0]['Instances'][0]['LaunchTime'])
                try:
                    status = self._ec2.describe_instance_status(InstanceIds=[instance.getInstanceId()])
                    instance.setStatus(status['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status'].title())
                except:
                    instance.setStatus("-")

                print("Instance "+str(count)+":  "+instance.getInstanceId())
                print("Lifecycle State: "+instance.getLifecycleState()+" - "+instance.getHealthStatus()+" - "+instance.getStatus())
                #print("Launch Time: "+instance.getLaunchTime().strftime('%m/%d/%Y %H:%M:%S'))
        
                try:
                    cpuUtilization = round(float(cpu['Datapoints'][0]['Maximum']),4)
                    print("CPU Usage: "+str(cpuUtilization)+"%")
                    instance.setCpuUtilization(cpuUtilization)
                except:
                    cpuUtilization = None
                
                try:
                    netIn = str(float(networkIn['Datapoints'][0]['Maximum'])/1000) # valor em kB
                    print("Network In: "+netIn+"Kb")
                    instance.setNetworkIn(netIn)
                except:
                    netIn = None
                
                try:
                    netOut = str(float(networkOut['Datapoints'][0]['Maximum'])/1000) # valor em kB
                    print("Network Out: "+netOut+"Kb")
                    instance.setNetworkOut(netOut)
                except:
                    netOut = None
                
                try:
                    packetin = str(networkPacketsIn['Datapoints'][0]['Average'])
                    print("Network Packages In: "+packetin)
                    instance.setNetworkPacketsIn(packetin)
                except:
                    packetin = None
                
                try:
                    packetout = str(networkPacketsOut['Datapoints'][0]['Average'])
                    print("Network Packages Out: "+packetout)
                    instance.setNetworkPacketsOut(packetout)
                except:
                    packetout = None

                if instance.getLifecycleState() == "Running" and instance.getHealthStatus() == "InService" and self._cooldown == False:
                    self.save_into_file(end_time, cpuUtilization, netIn, netOut, packetin, packetout, instance.getLifecycleState(), instance.getInstanceId())
                print()
        
        if self._cooldown == False:
            autoscaling = Autoscaling(self._instances, self._auto_scaling_group, self._asg, cpuUtilization, netIn, netOut)
            autoscaling.process()
            self._cooldown = autoscaling._cooldown
        else:
            self._cooldown_trigger +=1
            print("Cooldown "+str(self._cooldown_trigger))
            if self._cooldown_trigger == 4:
                self._cooldown = False
                self._cooldown_trigger = 0
        self.describe()

    def scale_up(self):
        self._asg.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + 1))
        print("Autoscaling Group scalled up, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() + 1)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() + 1))
    
    def scale_down(self):
        self._asg.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - 1))
        print("Autoscaling Group scalled down, from "+str(self._auto_scaling_group.getDesiredCapacity())+" to "+str(self._auto_scaling_group.getDesiredCapacity() - 1)+" new desired capacity: "+str(self._auto_scaling_group.getDesiredCapacity() - 1))


if __name__ == '__main__':
    app = App("engine-asg", "sa-east-1")
    
    try:
        if sys.argv[1] == "up":
            app.scale_up()
        if sys.argv[1] == "down":
            app.scale_down()
    except:
        app.read_instances()