from Hysys import Hysys
import Costing
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def run():
    case = Hysys('base case opt_editing.hsc')
    feed = case.getStream("Feed")
    col = case.getCol('T-100')
    recyclehx = case.getHX('E-100')
    feedpump = case.getPump('P-100')
    recyclepump = case.getPump('P-101')

    def getTAC():

        col_height = case.case.UtilityObjects.Item('Internals-1@Main Tower@COL1').SectionHeight.Values[0]

        cond = case.getSimpleHX('E-101', col.getTemperature()[0], col.getCondTemp(), col.getPressure()[0], col.getCondPressure())
        reboiler = case.getSimpleHX('E-102', col.getTemperature()[-1], col.getReboilTemp(), col.getPressure()[-1], col.getReboilPressure())


        colcost = Costing.Column(col.getDiameter(), col_height, max(col.getPressure()), max(col.getTemperature()), col.getTrays())
        condcost = Costing.HeatExchanger(cond.getDuty(), cond.getLMTD(), cond.getPressure())
        reboilcost = Costing.HeatExchanger(reboiler.getDuty(), reboiler.getLMTD(), reboiler.getPressure(), u=1140)
        recyclecoolcost = Costing.HeatExchanger(recyclehx.getDuty(), recyclehx.getLMTD(), recyclehx.getPressure())
        feedpumpcost = Costing.Pump(feedpump.getDuty(), feedpump.getPressure())
        recyclepumpcost= Costing.Pump(recyclepump.getDuty(), recyclepump.getPressure())

        capcost = [1.18 * i for i in [colcost.calculateBMC()/3, condcost.calculateBMC()/3, reboilcost.calculateBMC(fm=1.81)/3, recyclecoolcost.calculateBMC()/3, recyclepumpcost.calculateBMC()/3, feedpumpcost.calculateBMC()/3]]
        opcost = [reboilcost.calculateMPSteam(), condcost.calculateCoolingWater() + recyclecoolcost.calculateCoolingWater(), feedpumpcost.calculateElectrical() + recyclepumpcost.calculateElectrical()]

        # print()
        # print("Column cost: ${:,}".format(round(capcost[0])))
        # print("Condenser cost: ${:,}".format(round(capcost[1])))
        # print("Reboiler cost: ${:,}".format(round(capcost[2])))
        # print("Recycle HX cost: ${:,}".format(round(capcost[3])))
        # print("Recycle pump cost: ${:,}".format(round(capcost[4])))
        # print("Feed pump cost: ${:,}".format(round(capcost[5])))
        # print("Annual Capital cost: ${:,}".format(round(sum(capcost))))

        # print()
        # print("MP Steam cost: ${:,}".format(round(opcost[0])))
        # print("Cooling water cost: ${:,}".format(round(opcost[1])))
        # print("Electricity cost: ${:,}".format(round(opcost[2])))

        # print("Annual Operating cost: ${:,}".format(round(sum(opcost))))

        # print("TAC: ${:,}".format(round(sum(opcost + capcost))))
        return sum(opcost + capcost)

    df = pd.DataFrame()

    for i in range(1,97):
        print(f"Running stage {i}")

        case.setSolver(False)
        col.setFeed(feed, i)
        col.getSpec('ANE recovery').IsActive = False
        col.getSpec('Reflux ratio').IsActive = True
        col.getSpec('Reflux ratio').IsActive = False
        col.getSpec('ANE recovery').IsActive = True
        case.setSolver(True)
        col.run()

        for _ in range(3):
            if not col.isConverged():
                print(f"Error at stage {i}: Trying with reflux spec")
                case.setSolver(False)
                col.setFeed(feed, i)
                col.getSpec('ANE recovery').IsActive = False
                col.getSpec('Reflux ratio').IsActive = False
                col.getSpec('Reflux ratio').IsActive = True
                case.setSolver(True)
                col.run()
            
                if col.isConverged():
                    print(f"Stage {i} converged with reflux spec, trying back main spec")
                    case.setSolver(False)
                    col.setFeed(feed, i)
                    col.getSpec('ANE recovery').IsActive = False
                    col.getSpec('Reflux ratio').IsActive = True
                    col.getSpec('Reflux ratio').IsActive = False
                    col.getSpec('ANE recovery').IsActive = True
                    case.setSolver(True)
                    col.run()

                    if not col.isConverged():
                        print(f"Error at stage {i}: Trying back with reflux spec")
                        case.setSolver(False)
                        col.setFeed(feed, i)
                        col.getSpec('ANE recovery').IsActive = False
                        col.getSpec('Reflux ratio').IsActive = False
                        col.getSpec('Reflux ratio').IsActive = True
                        case.setSolver(True)
                        col.run()

        if not col.isConverged():
            print(f"Error at stage {i} Skipping stage")
        else:
            df = df.append([[i, getTAC(), col.getSpecValue("ANE recovery"), col.getSpecValue("ENE recovery"), col.getSpecValue("DMF recovery")]])

    df.columns = ["Stage", "TAC", "ANE recovery", "ENE recovery", "DMF recovery"]
    df.to_csv("varyfeed.csv")
