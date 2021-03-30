from subprocess import Popen, PIPE
import json, os
import xlsxwriter
from typing import Any
from AutoScalingGroup import AutoScalingGroup, Instance, AvailabilityZone, LoadBalancer, EnabledMetric, Tags

class AutoScaling():

    def __init__(self, autoscalinggroup, region):

        self._auto_scaling_info = dict()
        self._auto_scaling_group = AutoScalingGroup()
        self._instances = []

        self.describe(autoscalinggroup, region)
        self.build_auto_scaling_group()

    def json_converter(self, output):
        return json.loads(output)

    def describe(self, autoscalinggroup, region):
        p = Popen(['bat-files\describe-auto-scaling-group.bat', autoscalinggroup, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = p.communicate()[0]
        result = output.decode('utf-8').split("--region sa-east-1")
        
        self._auto_scaling_info = self.json_converter(result[1])

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
            
                workbook.close()

    def process(self):
        for instance in self._instances:
            print(instance.getInstanceId())

if __name__ == '__main__':
    autoscaling = AutoScaling("web-app-asg", "sa-east-1")
    autoscaling.create_files()
