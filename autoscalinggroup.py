class AutoScalingGroup():
    
    def __init__(self):
        self._autoScalingGroupName = ""
        self._autoScalingGroupARN = ""
        self._launchConfigurationName = ""
        self._minSize = ""
        self._maxSize = ""
        self._desiredCapacity = ""
        self._defaultCooldown = ""
        self._availabilityZones = []
        self._loadBalancerNames = []
        self._targetGroupARNs = []
        self._healthCheckType = ""
        self._healthCheckGracePeriod = ""
        self._instances = [Instance]
        self._createdTime = ""
        self._suspendedProcesses = []
        self._vpcZoneIdentifier = ""
        self._enabledMetrics = []
        self._tags = []
        self._terminationPolicies = []
        self._newInstancesProtectedFromScaleIn = ""
        self._serviceLinkedRoleARN = ""
        self._instanceIds = []

    def appendInstanceId(self, id):
        self._instanceIds.append(id)

    def getInstanceId(self):
        return self._instanceIds

    def setAutoScalingGroupName(self, autoScalingGroupName):
        self._autoScalingGroupName = autoScalingGroupName
        
    def setAutoScalingGroupARN(self, autoScalingGroupARN):
        self._autoScalingGroupARN = autoScalingGroupARN

    def setLaunchConfigurationName(self, launchConfigurationName):
        self._launchConfigurationName = launchConfigurationName

    def setsetAutoScalingGroupARNinSize(self, minSize):
        self._minSize = minSize

    def setMinSize(self, minSize):
        self._minSize = minSize

    def setDesiredCapacity(self, desiredCapacity):
        self._desiredCapacity = desiredCapacity

    def setDefaultCooldown(self, defaultCooldown):
        self._defaultCooldown = defaultCooldown

    def setAvailabilityZones(self, availabilityZones):
        self._availabilityZones = availabilityZones

    def setLoadBalancerNames(self, loadBalancerNames):
        self._loadBalancerNames = loadBalancerNames

    def setTargetGroupARNs(self, targetGroupARNs):
        self._targetGroupARNs = targetGroupARNs

    def setHealthCheckType(self, healthCheckType):
        self._healthCheckType = healthCheckType

    def setHealthCheckGracePeriod(self, healthCheckGracePeriod):
        self._healthCheckGracePeriod = healthCheckGracePeriod

    def setInstances(self, instances):
        self._instances = instances

    def setCreatedTime(self, createdTime):
        self._createdTime = createdTime

    def setSuspendedProcesses(self, suspendedProcesses):
        self._suspendedProcesses = suspendedProcesses

    def setVpcZoneIdentifier(self, vpcZoneIdentifier):
        self._vpcZoneIdentifier = vpcZoneIdentifier

    def setEnabledMetrics(self, enabledMetrics):
        self._enabledMetrics = enabledMetrics

    def setTags(self, tags):
        self._tags = tags

    def setTerminationPolicies(self, terminationPolicies):
        self._terminationPolicies = terminationPolicies

    def setNewInstancesProtectedFromScaleIn(self, newInstancesProtectedFromScaleIn):
        self._newInstancesProtectedFromScaleIn = newInstancesProtectedFromScaleIn

    def setServiceLinkedRoleARN(self, serviceLinkedRoleARN):
        self._serviceLinkedRoleARN = serviceLinkedRoleARN

    def getAutoScalingGroupName(self):
        return self._autoScalingGroupName
        
    def getAutoScalingGroupARN(self):
        return self._autoScalingGroupARN

    def getLaunchConfigurationName(self):
        return self._launchConfigurationName

    def getMinSize(self):
        return self._minSize

    def getMinSize(self):
        return self._minSize

    def getDesiredCapacity(self):
        return self._desiredCapacity

    def getDefaultCooldown(self):
        return self._defaultCooldown

    def getAvailabilityZones(self):
        return self._availabilityZones

    def getLoadBalancerNames(self):
        return self._loadBalancerNames

    def getTargetGroupARNs(self):
        return self._targetGroupARNs

    def getHealthCheckType(self):
        return self._healthCheckType

    def getHealthCheckGracePeriod(self):
        return self._healthCheckGracePeriod

    def getInstances(self):
        return self._instances

    def getCreatedTime(self):
        return self._createdTime

    def getSuspendedProcesses(self):
        return self._suspendedProcesses

    def getVpcZoneIdentifier(self):
        return self._vpcZoneIdentifier

    def getEnabledMetrics(self):
        return self._enabledMetrics

    def getTags(self):
        return self._tags

    def getTerminationPolicies(self):
        return self._terminationPolicies

    def getNewInstancesProtectedFromScaleIn(self):
        return self._newInstancesProtectedFromScaleIn

    def getServiceLinkedRoleARN(self):
        return self._serviceLinkedRoleARN

class Instance:
    
    def __init__(self):
        self._instanceId = ""
        self._instanceType = ""
        self._availabilityZone = ""
        self._lifecycleState = ""
        self._healthStatus = ""
        self._launchConfigurationName = ""
        self._protectedFromScaleIn = ""
        self._cpuUtilization = 0.0
        self._networkIn = 0.0
        self._networkOut = 0.0
        self._networkPacketsIn = 0.0
        self._networkPacketsOut = 0.0
        self._triggerUp = 0
        self._triggerDown = 0
        self._launchTime = ""
        self._status = ""
        self._network = 0.0

    def setInstanceId(self,instanceId):
        self._instanceId = instanceId

    def setInstanceType(self,instanceType):
        self._instanceType = instanceType

    def setAvailabilityZone(self,availabilityZone):
        self._availabilityZone = availabilityZone

    def setLifecycleState(self,lifecycleState):
        self._lifecycleState = lifecycleState

    def setHealthStatus(self,healthStatus):
        self._healthStatus = healthStatus

    def setLaunchConfigurationName(self,launchConfigurationName):
        self._launchConfigurationName = launchConfigurationName

    def setProtectedFromScaleIn(self, protectedFromScaleIn):
        self._protectedFromScaleIn = protectedFromScaleIn
    
    def getInstanceId(self):
       return self._instanceId

    def getInstanceType(self):
       return self._instanceType

    def getAvailabilityZone(self):
       return self._availabilityZone

    def getLifecycleState(self):
       return self._lifecycleState

    def getHealthStatus(self):
       return self._healthStatus

    def getLaunchConfigurationName(self):
       return self._launchConfigurationName

    def getProtectedFromScaleIn(self):
       return self._protectedFromScaleIn

    def setCpuUtilization(self, cpuUtilization):
        self._cpuUtilization = cpuUtilization
    
    def setNetworkIn(self, networkIn):
        self._networkIn = networkIn
        
    def setNetwork(self, network):
        self._network = network
    
    def setNetworkOut(self, networkOut):
        self._networkOut = networkOut
    
    def setNetworkPacketsIn(self, networkPacketsIn):
        self._networkPacketsIn = networkPacketsIn
    
    def setNetworkPacketsOut(self, networkPacketsOut):
        self._networkPacketsOut = networkPacketsOut

    def getCpuUtilization(self):
        return self._cpuUtilization
    
    def getNetworkIn(self):
        return self._networkIn
    
    def getNetwork(self):
        return self._network
    
    def getNetworkOut(self):
        return self._networkOut
    
    def getNetworkPacketsIn(self):
        return self._networkPacketsIn
    
    def getNetworkPacketsOut(self):
        return self._networkPacketsOut
    
    def incrementTriggerUp(self):
        self._triggerUp +=1

    def getTriggerUp(self):
        return self._triggerUp
    
    def clearTriggerUp(self):
        self._triggerUp = 0
    
    def incrementTriggerDown(self):
        self._triggerDown +=1

    def getTriggerDown(self):
        return self._triggerDown
    
    def clearTriggerDown(self):
        self._triggerDown = 0
    
    def setLaunchTime(self, launchtime):
        self._launchTime = launchtime
    
    def getLaunchTime(self):
        return self._launchTime

    def setStatus(self, status):
        self._status = status
    
    def getStatus(self):
        return self._status

class AvailabilityZone():
    def __init__(self):
        self._availabilityZone = ""

    def setAvailabilityZone(self, availabilityZone):
       self._availabilityZone = availabilityZone

    def getAvailabilityZone(self):
       return self._availabilityZone

class LoadBalancer():
    def __init__(self):
        self._loadBalancer = ""

    def setLoadBalancer(self, loadBalancer):
       self._loadBalancer = loadBalancer

    def getLoadBalancer(self):
       return self._loadBalancer

class EnabledMetric():
    def __init__(self):
        self._enabledMetric = ""
        self._granularity = ""

    def setEnabledMetric(self, enabledMetric):
       self._enabledMetric = enabledMetric

    def getEnabledMetric(self):
       return self._enabledMetric

    def setGranularity(self, granularity):
       self._granularity = granularity

    def getGranularity(self):
       return self._granularity

class Tags():
    def __init__(self):
        self._resourceId = ""
        self._resourceType = ""
        self._key = ""
        self._value = ""
        self._propagateAtLaunch = ""

    def setResourceId(self, resourceId):
       self._resourceId = resourceId

    def getResourceId(self):
       return self._resourceId

    def setResourceType(self, resourceType):
       self._resourceType = resourceType

    def getResourceType(self):
       return self._resourceType

    def setKey(self, key):
       self._key = key

    def getKey(self):
       return self._key

    def setValue(self, value):
       self._value = value

    def getValue(self):
       return self._value
    
    def setPropagateAtLaunch(self, propagateAtLaunch):
       self._propagateAtLaunch = propagateAtLaunch

    def getPropagateAtLaunch(self):
       return self._propagateAtLaunch