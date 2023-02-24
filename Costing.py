import math

# psig
def calculateDesignPressure(pressure):
    if 5 > pressure > 0:
        return 10
    elif pressure > 1000:
        return 1.1 * pressure
    elif pressure > 0:
        return math.exp(0.60608 + 0.91615 * math.log(pressure) + 0.0015655 * (math.log(pressure) ** 2))
    return None
    
def calculateStress(temperature):
    if temperature <= 750:
        return 15000
    elif temperature <= 800:
        return 14750
    elif temperature <=850:
        return 14200
    elif temperature <= 900:
        return 13100
    return None

# d in inches
def calculateMinWallThickness(d):
    d /= 12
    if d < 4:
        return 1/4
    elif d < 6:
        return 5/16
    elif d < 8:
        return 3/8
    elif d < 10:
        return 7/16
    return 1/2

# d in inches
# l in inches
def calculateWallThickness(p, d, s, l):
    t_s_possible = [i/16 for i in range(3,9)] + [i/8 for i in range(5,17)] + [i/4 for i in range(9, 13)]
    t_min = calculateMinWallThickness(d)
    if t_min >= 1.25:
        t_p = max(t_min, p*d/(2*s-1.2*p))
    else:
        t = max(t_min, p*d/(2*s*0.8-1.2*p))
        if t >= 1.25:
            assert max(t_min, p*d/(2*s-1.2*p)) >= 1.25
            t_p = max(t_min, p*d/(2*s-1.2*p))
        else:
            t_p = t

    for t_s in t_s_possible:
        d_o = d + t_s * 2
        t_v = t_p + 0.22*(d_o+18)*(l**2)/(2*s*(d_o**2))
        t_s_calc = t_v + 1/8
        if t_s_calc <= t_s:
            return t_s
        
    return None


class Column():

    '''
    Costing for tray column using carbon steel
    '''

    def __init__(self, diameter, height, pressure, temperature, trays):
        
        '''
        Pressure in kPa
        
        Temperature in C

        Diameter in m
        
        height in m

        '''

        self.diameter = diameter
        self.height = height
        self.trays = trays
        self.pressure = calculateDesignPressure((pressure- 101.325)/6.895) # psig
        self.temperature = (temperature * 9/5) + 32 + 50 # F

        self.stress = calculateStress(self.temperature)

        self.thickness = calculateWallThickness(self.pressure, diameter * 39.37, self.stress, height * 39.37) # inch


    def calculateBMC(self):
        v = self.diameter**2 * self.height * math.pi / 4
        if v < 0.3 or v > 520:
            # # print(f"Warning: Vessel volume is {v} m3, outside of interpolation range [0.3, 520]\n Using Six-Tenth Rule")
            if v < 0.3:
                a = 0.3
            else:
                a = 520
            cp = 10 ** (3.4974 + 0.4485*math.log10(a) + 0.1074*(math.log10(a)**2)) * 816.3 / 397
            cp = (v/a) ** 0.6 * cp
        else:
            cp = 10 ** (3.4974 + 0.4485*math.log10(v) + 0.1074*(math.log10(v)**2)) * 816.3 / 397 #

        if self.thickness < 0.25:
            fp = 1
        else:
            fp = ((self.pressure / 14.5037738 + 1) * (self.diameter)/ (2*(850-0.6*(self.pressure / 14.5037738 + 1))) + 0.00315)/0.0063

        fbm = 2.25 + 1.82*fp*1

        cbm = fbm*cp

        tray_area = self.diameter**2 * math.pi / 4

        if tray_area < 0.07 or tray_area > 12.30:
            # # print(f"Warning: Tray area is {tray_area} m2, outside of interpolation range [0.07, 12.3]\n Using Six-Tenth Rule")
            if tray_area < 0.07:
                a = 0.07
            else:
                a = 12.30
            cp_t = 10 ** (2.9949 + 0.4465*math.log10(a) + 0.3961*(math.log10(a)**2)) * 816.3 / 397
            cp_t = (tray_area/a) ** 0.6 * cp_t
        else:
            cp_t = 10 ** (2.9949 + 0.4465*math.log10(tray_area) + 0.3961*(math.log10(tray_area)**2)) * 816.3 / 397

        if self.trays >= 20:
            cbm_tray = cp_t*self.trays*1*1
        else:
            cbm_tray = cp_t*self.trays*1*10**(0.4471 + 0.08516*math.log10(self.trays) - 0.3474*(math.log10(self.trays)**2))

        return cbm_tray + cbm
    
class HeatExchanger():
    '''

    For floating head
    
    '''

    def __init__(self, duty, lmtd, p, u=850, f=0.9) -> None:
        '''
        duty in kw
        pressure in kpa
        for reboiler set u to 1140
        '''
        self.duty = duty
        self.u = u
        self.lmtd = lmtd
        self.f = f
        self.a = duty*1000/(u*f*lmtd)
        self.p = (p- 101.325)/100
    
    def calculateBMC(self, fm=1.35):
        if self.a < 10 or self.a > 1000:
            # # print(f"Warning: HX area is {self.a} m2, outside of interpolation range [10, 1000]\n Using Six-Tenth Rule")
            if self.a < 10:
                a = 10
            else:
                a = 1000
            cp = 10 ** (4.8306 - 0.8509*math.log10(a) + 0.3187*((math.log10(a))**2)) * 816.3 / 397
            cp = (self.a/a) ** 0.6 * cp
        else:
            cp = 10 ** (4.8306 - 0.8509*math.log10(self.a) + 0.3187*((math.log10(self.a))**2)) * 816.3 / 397

        if self.p > 5:
            fp = 10**(0.03881 - 0.11272*math.log10(self.p) + 0.08183*((math.log10(self.p))**2))
        else:
            fp = 1

        return cp*(1.63 + 1.66*fp*fm)
    
    def calculateMPSteam(self, hours=8256):
        return self.duty / 1000000 * 60 * 60 * hours * 4.77
    
    def calculateCoolingWater(self, hours=8256):
        '''
        Assumes return temp 40C
        '''
        return self.duty / 1000000 * 60 * 60 * hours * 0.378
    
class Pump():
    def __init__(self, power, pressure) -> None:
        self.power = power
        self.pressure = (pressure- 101.325)/100

    def calculateBMC(self):
        if self.power < 1 or self.power > 300:
            # # # print(f"Warning: pump power is {self.power} kW, outside of interpolation range [1, 300]\n Using Six-Tenth Rule")
            if self.power < 1:
                p = 1
            else:
                p = 300
            cp = 10 ** (3.3892 + 0.0536*math.log10(p) + 0.1538*((math.log(p))**2) * 816.3 / 397)
            cp = (self.power/p) ** 0.6 * cp 
        else:
            cp = 10 ** (3.3892 + 0.0536*math.log10(self.power) + 0.1538*((math.log(self.power))**2) * 816.3 / 397)

        if self.pressure > 10:
            fp = 10**(-0.3935 + 0.3957*math.log10(self.power) - 0.00226*((math.log10(self.power))**2))
        else:
            fp = 1

        return cp*(1.89 + 1.35 * 1.55 * fp)
    
    def calculateElectrical(self, hours=8256):
        return self.power * hours * 0.0674
