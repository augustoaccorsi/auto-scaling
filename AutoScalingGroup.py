
class AutoScalingGroup():

    autoScalingGroupName = ""
    autoScalingGroupARN = ""
    launchConfigurationName = ""
    minSize = ""
    maxSize = ""
    desiredCapacity = ""
    defaultCooldown = ""
    availabilityZones = []
    loadBalancerNames = []
    targetGroupARNs = []
    healthCheckType = ""
    healthCheckGracePeriod = ""
    instances = []
    createdTime = ""
    suspendedProcesses = []
    vpcZoneIdentifier = ""
    enabledMetrics = []
    tags = []
    terminationPolicies = []
    newInstancesProtectedFromScaleIn = ""
    serviceLinkedRoleARN = ""

    def setAutoScalingGroupName(self, autoScalingGroupName):
        self.autoScalingGroupName = autoScalingGroupName
        
    def setAutoScalingGroupARN(self, autoScalingGroupARN):
        self.autoScalingGroupARN = autoScalingGroupARN

    def setLaunchConfigurationName(self, launchConfigurationName):
        self.launchConfigurationName = launchConfigurationName

    def setsetAutoScalingGroupARNinSize(self, minSize):
        self.minSize = minSize

    def setMinSize(self, minSize):
        self.minSize = minSize

    def setDesiredCapacity(self, desiredCapacity):
        self.desiredCapacity = desiredCapacity

    def setDefaultCooldown(self, defaultCooldown):
        self.defaultCooldown = defaultCooldown

    def setAvailabilityZones(self, availabilityZones):
        self.availabilityZones = availabilityZones

    def setLoadBalancerNames(self, loadBalancerNames):
        self.loadBalancerNames = loadBalancerNames

    def setTargetGroupARNs(self, targetGroupARNs):
        self.targetGroupARNs = targetGroupARNs

    def setHealthCheckType(self, healthCheckType):
        self.healthCheckType = healthCheckType

    def setHealthCheckGracePeriod(self, healthCheckGracePeriod):
        self.healthCheckGracePeriod = healthCheckGracePeriod

    def setInstances(self, instances):
        self.instances = instances

    def setCreatedTime(self, createdTime):
        self.createdTime = createdTime

    def setSuspendedProcesses(self, suspendedProcesses):
        self.suspendedProcesses = suspendedProcesses

    def setVpcZoneIdentifier(self, vpcZoneIdentifier):
        self.vpcZoneIdentifier = vpcZoneIdentifier

    def setEnabledMetrics(self, enabledMetrics):
        self.enabledMetrics = enabledMetrics

    def setTags(self, tags):
        self.tags = tags

    def setTerminationPolicies(self, terminationPolicies):
        self.terminationPolicies = terminationPolicies

    def setNewInstancesProtectedFromScaleIn(self, newInstancesProtectedFromScaleIn):
        self.newInstancesProtectedFromScaleIn = newInstancesProtectedFromScaleIn

    def setServiceLinkedRoleARN(self, serviceLinkedRoleARN):
        self.serviceLinkedRoleARN = serviceLinkedRoleARN

    def getAutoScalingGroupName(self):
        return self.autoScalingGroupName
        
    def getAutoScalingGroupARN(self):
        return self.autoScalingGroupARN

    def getLaunchConfigurationName(self):
        return self.launchConfigurationName

    def getMinSize(self):
        return self.minSize

    def getMinSize(self):
        return self.minSize

    def getDesiredCapacity(self):
        return self.desiredCapacity

    def getDefaultCooldown(self):
        return self.defaultCooldown

    def getAvailabilityZones(self):
        return self.availabilityZones

    def getLoadBalancerNames(self):
        return self.loadBalancerNames

    def getTargetGroupARNs(self):
        return self.targetGroupARNs

    def getHealthCheckType(self):
        return self.healthCheckType

    def getHealthCheckGracePeriod(self):
        return self.healthCheckGracePeriod

    def getInstances(self):
        return self.instances

    def getCreatedTime(self):
        return self.createdTime

    def getSuspendedProcesses(self):
        return self.suspendedProcesses

    def getVpcZoneIdentifier(self):
        return self.vpcZoneIdentifier

    def getEnabledMetrics(self):
        return self.enabledMetrics

    def getTags(self):
        return self.tags

    def getTerminationPolicies(self):
        return self.terminationPolicies

    def getNewInstancesProtectedFromScaleIn(self):
        return self.newInstancesProtectedFromScaleIn

    def getServiceLinkedRoleARN(self):
        return self.serviceLinkedRoleARN

class Instance:
    
    instanceId = ""
    instanceType = ""
    availabilityZone = ""
    lifecycleState = ""
    healthStatus = ""
    launchConfigurationName = ""
    protectedFromScaleIn = ""

    def setInstanceId(self,instanceId):
        self.instanceId = instanceId

    def setInstanceType(self,instanceType):
        self.instanceType = instanceType

    def setAvailabilityZone(self,availabilityZone):
        self.availabilityZone = availabilityZone

    def setLifecycleState(self,lifecycleState):
        self.lifecycleState = lifecycleState

    def setHealthStatus(self,healthStatus):
        self.healthStatus = healthStatus

    def setLaunchConfigurationName(self,launchConfigurationName):
        self.launchConfigurationName = launchConfigurationName

    def setProtectedFromScaleIn(self, protectedFromScaleIn):
        self.protectedFromScaleIn = protectedFromScaleIn
    
    def getInstanceId(self):
       return self.instanceId

    def getInstanceType(self):
       return self.instanceType

    def getAvailabilityZone(self):
       return self.availabilityZone

    def getLifecycleState(self):
       return self.lifecycleState

    def getHealthStatus(self):
       return self.healthStatus

    def getLaunchConfigurationName(self):
       return self.launchConfigurationName

    def getProtectedFromScaleIn(self):
       return self.protectedFromScaleIn

class AvailabilityZone():
    availabilityZone = ""

    def setAvailabilityZone(self, availabilityZone):
       self.availabilityZone = availabilityZone

    def getAvailabilityZone(self):
       return self.availabilityZone

class LoadBalancer():
    loadBalancer = ""

    def setLoadBalancer(self, loadBalancer):
       self.loadBalancer = loadBalancer

    def getLoadBalancer(self):
       return self.loadBalancer

class EnabledMetric():
    enabledMetric = ""
    granularity = ""

    def setEnabledMetric(self, enabledMetric):
       self.enabledMetric = enabledMetric

    def getEnabledMetric(self):
       return self.enabledMetric

    def setGranularity(self, granularity):
       self.granularity = granularity

    def getGranularity(self):
       return self.granularity

class Tags():
    resourceId = ""
    resourceType = ""
    key = ""
    value = ""
    propagateAtLaunch = ""

    def setResourceId(self, resourceId):
       self.resourceId = resourceId

    def getResourceId(self):
       return self.resourceId

    def setResourceType(self, resourceType):
       self.resourceType = resourceType

    def getResourceType(self):
       return self.resourceType

    def setKey(self, key):
       self.key = key

    def getKey(self):
       return self.key

    def setValue(self, value):
       self.value = value

    def getValue(self):
       return self.value
    
    def setPropagateAtLaunch(self, propagateAtLaunch):
       self.propagateAtLaunch = propagateAtLaunch

    def getPropagateAtLaunch(self):
       return self.propagateAtLaunch