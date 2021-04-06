import json, os, xlsxwriter, datetime, timedelta, boto3
from openpyxl import load_workbook
from autoScalingGroup import AutoScalingGroup, Instance, AvailabilityZone, LoadBalancer, EnabledMetric, Tags
from autoscaling import Autoscaling

class App():

    #def __init__(self, autoscalinggroup, region, accessKeyId, secretAccessKey, sessionToken):
    def __init__(self, autoscalinggroup, region):
        
        
        self._asg = boto3.client('autoscaling', region_name=region)
        self._cloud_watch = boto3.client('cloudwatch',  region_name=region)

        #self._asg = boto3.client('autoscaling', region_name=region, aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey, aws_session_token=sessionToken)
        #self._cloud_watch = boto3.client('cloudwatch',  region_name=region, aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey, aws_session_token=sessionToken)

        self._auto_scaling_info = dict()
        self._auto_scaling_group = AutoScalingGroup()
        self._instances = []

        self.describe(autoscalinggroup).build_auto_scaling_group()

    def json_converter(self, output):
        return json.loads(output)
    
    def clear_all(self):
        self._auto_scaling_info = dict()
        self._auto_scaling_group = AutoScalingGroup()
        self._instances = []

    def describe(self, autoscalinggroup):
        if len(self._instances) > 0:
            self.clear_all()
        self._auto_scaling_info = self._asg.describe_auto_scaling_groups(AutoScalingGroupNames=[autoscalinggroup], MaxRecords=100)
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

        return loadBalancersList
    
    def build_instances(self, instances):
        intancesList = []
        for intance in instances:
            inst = Instance()
            inst.setInstanceId(intance['InstanceId'])
            inst.setInstanceType(intance['InstanceType'])
            inst.setAvailabilityZone(intance['AvailabilityZone'])
            inst.setLifecycleState(intance['LifecycleState'])
            inst.setHealthStatus(intance['HealthStatus'])
            inst.setLaunchConfigurationName(intance['LaunchConfigurationName'])
            inst.setProtectedFromScaleIn(intance['ProtectedFromScaleIn'])
            intancesList.append(inst)
            self._instances.append(inst)

        return intancesList

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

    def create_files(self):
        for instance in self._instances:
            if not os.path.isfile('data-set\\'+instance.getInstanceId()+'.xlsx'):
                workbook = xlsxwriter.Workbook('data-set\\'+instance.getInstanceId()+'.xlsx')
                worksheet = workbook.add_worksheet()
    
                worksheet.write('A1', 'Date')
                worksheet.write('B1', 'Hour')
                worksheet.write('C1', 'CPU Utilization')
                worksheet.write('D1', 'Network In')
                worksheet.write('E1', 'Network Out')
                worksheet.write('F1', 'Network Packets In')
                worksheet.write('G1', 'Network Packets Out')
                worksheet.write('H1', 'Lifecycle State')
            
                workbook.close()

    def save_into_file(self, date, hour, cpu, networkIn, networkOut, networkPacketsIn, networkPacketsOut, lifecycleState, instance):
        workbook = load_workbook(filename = 'data-set\\'+instance+'.xlsx')
        worksheet = workbook['Sheet1']
        
        newRowLocation = worksheet.max_row +1

        worksheet.cell(column=1,row=newRowLocation, value=date)
        worksheet.cell(column=2,row=newRowLocation, value=hour)
        if cpu != None:
            worksheet.cell(column=3,row=newRowLocation, value=cpu)
        if networkIn != None:
            worksheet.cell(column=4,row=newRowLocation, value=networkIn)
        if networkOut != None:
            worksheet.cell(column=5,row=newRowLocation, value=networkOut)
        if networkPacketsIn != None:
            worksheet.cell(column=6,row=newRowLocation, value=networkPacketsIn)
        if networkPacketsOut != None:
            worksheet.cell(column=7,row=newRowLocation, value=networkPacketsOut)
        if lifecycleState != None:
            worksheet.cell(column=8,row=newRowLocation, value=lifecycleState)

        workbook.save(filename = 'data-set\\'+instance+'.xlsx')
        workbook.close()


    def get_metric(self, metric, instance, start_time, end_time, statistics):
        return self._cloud_watch.get_metric_statistics(Namespace='AWS/EC2',
            MetricName=metric,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance
                },
            ], StartTime=start_time, EndTime=end_time, Period=60, Statistics=[statistics]) 

    def read_instances(self):
        for instance in self._instances:
            end_time = datetime.datetime.utcnow()
            
            start_time = end_time - datetime.timedelta(seconds=120)

            start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
         
            cpu =  self.get_metric("CPUUtilization", instance.getInstanceId(), start_time, end_time, "Maximum")
            networkIn =  self.get_metric("NetworkIn", instance.getInstanceId(), start_time, end_time, "Maximum")
            networkOut =  self.get_metric("NetworkOut", instance.getInstanceId(), start_time, end_time, "Maximum")
            networkPacketsIn =  self.get_metric("NetworkPacketsIn", instance.getInstanceId(), start_time, end_time, "Average")
            networkPacketsOut =  self.get_metric("NetworkPacketsOut", instance.getInstanceId(), start_time, end_time, "Average")
    
            date_hour = end_time.split("T")
            
            print("Instance "+instance.getInstanceId())
            print("Lifecycle State: "+instance.getLifecycleState())
    
            if(instance.getLifecycleState() == "InService"):
                try:
                    cpuUtilization = round(float(cpu['Datapoints'][0]['Maximum']),4)
                    print("CPU Usage: "+str(cpuUtilization)+"%")
                    instance.setCpuUtilization(cpuUtilization)
                except:
                    cpuUtilization = None
                
                try:
                    netIn = str(networkIn['Datapoints'][0]['Maximum'])
                    print("Network In: "+netIn+" bytes")
                    instance.setNetworkIn(netIn)
                except:
                    netIn = None
                
                try:
                    netOut = str(networkOut['Datapoints'][0]['Maximum'])
                    print("Network Out: "+netOut+" bytes")
                    instance.setNetworkOut(netOut)
                except:
                    netOut = None
                
                try:
                    packetIn = str(networkPacketsIn['Datapoints'][0]['Average'])
                    print("Network Packages In: "+packetIn)
                    instance.setNetworkPacketsIn(packetIn)
                except:
                    packetIn = None
                
                try:
                    packetOut = str(networkPacketsOut['Datapoints'][0]['Average'])
                    print("Network Packages Out: "+packetOut)
                    instance.setNetworkPacketsOut(packetOut)
                except:
                    packetOut = None

                self.save_into_file(date_hour[0], date_hour[1][:-1], cpuUtilization, netIn, netOut, packetIn, packetOut, instance.getLifecycleState(), instance.getInstanceId())

        autoscaling = Autoscaling(self._instances, self._auto_scaling_group, self._asg)

        if autoscaling.process() == True:
            self.describe(self._auto_scaling_group.getAutoScalingGroupName()).build_auto_scaling_group()
   
    def scale_up(self):
        response = self._asg.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() + 1))
        print(response)
    
    def scale_down(self):
        response = self._asg.set_desired_capacity(AutoScalingGroupName=self._auto_scaling_group.getAutoScalingGroupName(), DesiredCapacity=(self._auto_scaling_group.getDesiredCapacity() - 1))
        print(response)

if __name__ == '__main__':
    app = App("engine-asg", "sa-east-1")
    app.create_files()
    app.read_instances()
    print("-----")
    app.create_files()
    app.read_instances()
    print("-----")
    app.create_files()
    app.read_instances()
    print("-----")
    app.create_files()
    app.read_instances()
    #app.scale_up()
    #app.scale_down()