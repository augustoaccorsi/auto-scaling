from subprocess import Popen, PIPE
import json
from typing import Any
from AutoScalingGroup import AutoScalingGroup, Instance, AvailabilityZone, LoadBalancer, EnabledMetric, Tags

class AutoScaling():

    auto_scaling_info = dict()
    auto_scaling_group = AutoScalingGroup()
    instances = []

    def __init__(self, autoscalinggroup, region):
        self.describe(autoscalinggroup, region)
        self.build_auto_scaling_group()

    def json_converter(self, output):
        return json.loads(output)

    def describe(self, autoscalinggroup, region):
        p = Popen(['bat-files\describe-auto-scaling-group.bat', autoscalinggroup, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = p.communicate()[0]
        result = output.decode('utf-8').split("--region sa-east-1")
        
        self.auto_scaling_info = self.json_converter(result[1])

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
            self.instances.append(inst)

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
        self.auto_scaling_group.setAutoScalingGroupName(self.auto_scaling_info['AutoScalingGroups'][0]['AutoScalingGroupName'])
        self.auto_scaling_group.setAutoScalingGroupARN(self.auto_scaling_info['AutoScalingGroups'][0]['AutoScalingGroupARN'])
        self.auto_scaling_group.setLaunchConfigurationName(self.auto_scaling_info['AutoScalingGroups'][0]['LaunchConfigurationName'])
        self.auto_scaling_group.setMinSize(self.auto_scaling_info['AutoScalingGroups'][0]['MinSize'])
        self.auto_scaling_group.setMinSize(self.auto_scaling_info['AutoScalingGroups'][0]['MaxSize'])
        self.auto_scaling_group.setDesiredCapacity(self.auto_scaling_info['AutoScalingGroups'][0]['DesiredCapacity'])
        self.auto_scaling_group.setDefaultCooldown(self.auto_scaling_info['AutoScalingGroups'][0]['DefaultCooldown'])
        self.auto_scaling_group.setAvailabilityZones(self.build_availability_zones(self.auto_scaling_info['AutoScalingGroups'][0]['AvailabilityZones']))
        self.auto_scaling_group.setLoadBalancerNames(self.build_load_balancers(self.auto_scaling_info['AutoScalingGroups'][0]['LoadBalancerNames']))
        self.auto_scaling_group.setTargetGroupARNs(self.auto_scaling_info['AutoScalingGroups'][0]['TargetGroupARNs'])
        self.auto_scaling_group.setHealthCheckType(self.auto_scaling_info['AutoScalingGroups'][0]['HealthCheckType'])
        self.auto_scaling_group.setHealthCheckGracePeriod(self.auto_scaling_info['AutoScalingGroups'][0]['HealthCheckGracePeriod'])
        self.auto_scaling_group.setInstances(self.auto_scaling_info['AutoScalingGroups'][0]['Instances'])
        self.auto_scaling_group.setCreatedTime(self.auto_scaling_info['AutoScalingGroups'][0]['CreatedTime'])
        self.auto_scaling_group.setSuspendedProcesses(self.auto_scaling_info['AutoScalingGroups'][0]['SuspendedProcesses'])
        self.auto_scaling_group.setVpcZoneIdentifier(self.auto_scaling_info['AutoScalingGroups'][0]['VPCZoneIdentifier'])
        self.auto_scaling_group.setEnabledMetrics(self.biuld_metrics(self.auto_scaling_info['AutoScalingGroups'][0]['EnabledMetrics']))
        self.auto_scaling_group.setTags(self.build_tags(self.auto_scaling_info['AutoScalingGroups'][0]['Tags']))
        self.auto_scaling_group.setTerminationPolicies(self.auto_scaling_info['AutoScalingGroups'][0]['TerminationPolicies'])
        self.auto_scaling_group.setNewInstancesProtectedFromScaleIn(self.auto_scaling_info['AutoScalingGroups'][0]['NewInstancesProtectedFromScaleIn'])
        self.auto_scaling_group.setServiceLinkedRoleARN(self.auto_scaling_info['AutoScalingGroups'][0]['ServiceLinkedRoleARN'])

        

if __name__ == '__main__':
    autoscaling = AutoScaling("web-app-asg", "sa-east-1")
