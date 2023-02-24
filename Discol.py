class Discol():
    def __init__(self, col):
        self.col = col

    def setTrays(self, num):
        self.col.ColumnFlowsheet.Operations.Item('Main Tower').NumberOfTrays = num
    
    def run(self):
        self.col.ColumnFlowsheet.Run()

    def setFeed(self, feed, num):
        f = self.col.ColumnFlowsheet.FeedStreams.Item(feed.stream.name)
        self.col.ColumnFlowsheet.Operations.Item("Main Tower").SpecifyFeedLocation(f, num)

    def isConverged(self):
        return self.col.ColumnFlowsheet.CfsConverged
    
    def getTrays(self):
        return self.col.ColumnFlowsheet.Operations.Item('Main Tower').NumberOfTrays
    
    def getDiameter(self):
        # Returns in m
        return self.col.ColumnFlowsheet.Operations.Item('Main Tower').ColumnDiameterValue
    
    def getPressure(self):
        # Returns in kPa
        return self.col.ColumnFlowsheet.Operations.Item('Main Tower').PressureValue

    def getTemperature(self):
        # Returns in C
        return self.col.ColumnFlowsheet.Operations.Item('Main Tower').TemperatureValue
    
    def getCondTemp(self):
        return self.col.ColumnFlowsheet.Operations.Item('Condenser').VesselTemperatureValue
    
    def getCondPressure(self):
        return self.col.ColumnFlowsheet.Operations.Item('Condenser').VesselPressureValue
    
    def getReboilTemp(self):
        return self.col.ColumnFlowsheet.Operations.Item('Reboiler').VesselTemperatureValue
    
    def getReboilPressure(self):
        return self.col.ColumnFlowsheet.Operations.Item('Reboiler').VesselPressureValue
    
    def getSpec(self, specname):
        return self.col.ColumnFlowsheet.Specifications.Item(specname)
    
    def getSpecValue(self, specname):
        return self.col.ColumnFlowsheet.Specifications.Item(specname).CurrentValue