import win32com.client as win32
import os
from Stream import Stream
from Discol import Discol
from Pump import Pump
from HX import *

class Hysys():
    def __init__(self, file):
        hysys = win32.Dispatch('Hysys.Application.V12.1')
        p = os.path.join(os.getcwd(), file)
        case = hysys.SimulationCases.Open(p)
        self.case = case

    def getStream(self, name):
        return Stream(self.case.Flowsheet.MaterialStreams.Item(name))
    
    def getCol(self, name):
        return Discol(self.case.Flowsheet.Operations.Item(name))

    def getHX(self, name):
        return HX(self.case.Flowsheet.Operations.Item(name))
    
    def getSimpleHX(self, name, tin, tout, pin, pout):
        return SimpleHX(self.case.Flowsheet.Operations.Item(name), tin, tout, pin, pout)
    
    def getPump(self, name):
        return Pump(self.case.Flowsheet.Operations.Item(name))
    
    def setSolver(self, set):
        self.case.Solver.CanSolve = set