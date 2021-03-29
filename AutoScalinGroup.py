import Instance

class AutoScalingGroup:

    autoScalingGroupName = ""
    atoScalingGroupARN = ""
    launchConfigurationName = ""
    minSize = ""
    maxSize = ""
    desiredCapacity = ""
    defaultCooldown = ""
    availabilityZones = []
    loadBalancerNames = [ ]
    targetGroupARNs = []
    healthCheckType = ""
    healthCheckGracePeriod = ""
    instances = []
    createdTime = ""
    suspendedProcesses = []
    vpcZoneIdentifier = ""
    enabledMetrics = []
    tags = [ ]
    terminationPolicies = []
    newInstancesProtectedFromScaleIn = ""
    serviceLinkedRoleARN = ""