class Stream():
    def __init__(self, stream):
        self.stream = stream
    
    def getComp(self):
        names = self.stream.ComponentMolarFraction.OffsetNames[0]
        vals = self.stream.ComponentMolarFraction.Values
        return {name : val for name, val in zip(names, vals)}

    def setP(self, val):
        self.stream.Pressure.SetValue(val)

    def setT(self, val):
        self.stream.Temperature.SetValue(val)

    def getVolFlow(self):
        '''
        returns in m^3/h
        '''
        return self.stream.ActualVolumeFlowValue*3600
    
    def getMassFlow(self):
        '''
        kg/h
        '''
        return self.stream.MassFlowValue*3600