class Pump():
    def __init__(self, pump) -> None:
        self.pump = pump

    def getDuty(self):
        '''
        kW
        '''
        return self.pump.EnergyStream.HeatFlowValue
    
    def getPressure(self):
        return max(self.pump.FeedPressureValue, self.pump.ProductPressureValue)
