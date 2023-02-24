import math

class HX():
    def __init__(self, hx) -> None:
        self.hx = hx
        assert self.hx.MinimumApproachValue >= 10

    def getDuty(self):
        '''
        in kW
        '''
        return self.hx.DutyValue
    
    def getLMTD(self):
        return self.hx.LmtdValue

    def MinimumApproachValue(self):
        return self.hx.MinimumApproachValue
    
    def getPressure(self):
        '''
        in kpa
        '''
        return max(self.hx.ShellSideProduct.PressureValue, self.hx.ShellSideFeed.PressureValue, self.hx.TubeSideFeed.PressureValue, self.hx.TubeSideProduct.PressureValue)
    

class SimpleHX():
    def __init__(self, hx, tin, tout, pin, pout) -> None:
        '''
        in C
        '''
        self.hx = hx
        self.pin = pin
        self.pout = pout
        self.t_end1 = tin
        self.t_end2 = tout
        self.t_end12 = self.hx.ProductTemperatureValue
        self.t_end22 = self.hx.FeedTemperatureValue
        assert min(abs(self.t_end1 - self.t_end12), abs(self.t_end2 - self.t_end22)) >= 10
        

    def getDuty(self):
        return self.hx.DutyValue
    
    def getLMTD(self):
        diff1 = abs(self.t_end1 - self.t_end12)
        diff2 = abs(self.t_end2 - self.t_end22)
        return (diff1 - diff2)/math.log(diff1/diff2)    
    
    def getPressure(self):
        '''
        in kpa
        '''
        return max(self.hx.FeedPressureValue, self.hx.ProductPressureValue, self.pin, self.pout)