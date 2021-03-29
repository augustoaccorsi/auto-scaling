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
