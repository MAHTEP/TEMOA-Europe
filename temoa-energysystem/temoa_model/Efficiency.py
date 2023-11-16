from pyomo.environ import *
from pyomo.core import Objective, Var, Constraint
from pyomo.opt import SolverFactory
import sys, os
from matplotlib import pyplot as plt
import numpy as np
from IPython import embed as IP
from temoa_model import temoa_create_model
from temoa_initialize import DemandConstraintErrorCheck
from temoa_rules import PeriodCost_rule

def parameters(dm_instance, iaux, time_fut, instance, dV_Capacity, price_data, alpha, sigma, P_theta, eps, PRICE_RANGE):
    #Fixing Capacity values for first stage at the ef instance with values from the deterministic instance
    if iaux != time_fut[0]:
        for i , j in dV_Capacity:
            if j < iaux and i in instance.tech_all.keys():
                instance.V_Capacity[i, j].fix(dV_Capacity[i,j])
    optimizer = SolverFactory('gurobi')
    results = optimizer.solve(instance, suffixes=['dual'])
    instance.solutions.load_from(results)

    for  p, s, d, dem  in sorted(instance.V_Demand.keys()):
        key =  p, s, d, dem
        if p == iaux:
            diff = []
            for z in sorted(instance.demand_segment.keys()):
                diff.append(value(instance.DemandSegment_midpoint[key, z]) - value(instance.V_Demand[key]))
            idx = (np.abs(diff)).argmin()
            elecDemand = value(instance.V_Demand[key])
            elecPrice  = value(instance.PriceSegment[key,idx+1])
            IP()
            phi = (elecDemand) / (elecPrice**(-sigma) * (1-alpha)**sigma * (alpha**sigma * P_theta**(1-sigma) + (1-alpha)**sigma * elecPrice**(1-sigma))**((eps + sigma)/(1 - sigma)))
            
            newPrice = (alpha**sigma * P_theta**(1-sigma) + (1-alpha)**sigma * elecPrice**(1-sigma))**(1/(1 - sigma))
            
            minESDemand = phi * newPrice**eps * 0.9

            print("%10g  %15s    %5s    %5s   %10g    %10g" %\
                        ( p, s, d, dem, phi, minESDemand),file=price_data)

def solve_dm(model, dat):
    #This function solves a deterministic model 
    model.dual  = Suffix(direction=Suffix.IMPORT)
    model.del_component('M.DemandActivityConstraint_psdtv_dem_s0d0')
    model.del_component('DemandActivityConstraint')
    data = DataPortal(model = model)
    data.load(filename=dat)
    instance = model.create_instance(data) #Defining the model instance with the data from .dat file
    optimizer = SolverFactory('gurobi')  #Defining the optimization solver
    results = optimizer.solve(instance, suffixes=['dual'])    #Solving the optimization model
    instance.solutions.load_from(results)
    DEMAND_RANGE = 0.95 # Max/MinDemand = (1 +/- DEMAND_RANGE)* Demand
    DEMAND_SEGMENTS = 71 # number of steps
    price_data = open("price.dat", "w") #create a new file
    
    ConstantDemandConstraint = instance.DemandConstraint
    Demand = instance.Demand
    
    print("""\
    data;
    
    param: MinDemand    MaxDemand  :=
        # year      # min    # max
    """, file=price_data)
    for key in sorted(Demand.sparse_keys()):
        if DEMAND_RANGE < 1.0:
            for l in key:
                print("%10s" % l,file=price_data)
            print("    %10g    %10g    " % \
                ((1 - DEMAND_RANGE) * Demand[key],
                 (1 + DEMAND_RANGE) * Demand[key]),file=price_data)
        else:
            for l in key:
                print("%10s" % l,file=price_data)
            print("    %10g    %10g    " % \
                (0.01,
                 (1 + DEMAND_RANGE) * Demand[key]),file=price_data)
    
    print("    ;\n",file=price_data)
    print("""\
    param: Price    Elast:=
        # year   # season   # time_of_day   # demand    # price    # elasticity
    """,file=price_data)
    #IP()
    for item in sorted(ConstantDemandConstraint.items()):
        price = instance.dual[item[1]]
        print("%10s    %10s    %10s    %10s    %10g    %10g    " % \
        (item[0][0], item[0][1], item[0][2], item[0][3], instance.dual[item[1]],1.1),file=price_data)
    
    print("    ;\n",file=price_data)
    print("param num_demand_segments := %d ;\
    # number of segments in the demand range" % DEMAND_SEGMENTS,file=price_data)
    price_data.close()
    return instance #Returning instance solved, values will be used later

def temoa_elastic(dat, dat1):
    M  = temoa_create_model()
    M.dual  = Suffix(direction=Suffix.IMPORT)
    M.lrc   = Suffix(direction=Suffix.IMPORT)
    M.urc   = Suffix(direction=Suffix.IMPORT)
    
    def TotalWelfare_rule ( M ):
    
        consumer_costs = sum(( value(M.DemandSegment_bound_value[ p, s, d, dem]) - M.V_DemandSegment[ p, s, d, dem, z])
           * value(M.PriceSegment[ p, s, d, dem, z])
           for ( p, s, d, dem, z) in M.DemandConstraint_rpsdcz)

        producer_costs = sum( PeriodCost_rule(M, p) for p in M.time_optimize )
        return (producer_costs - consumer_costs)
    
    # ELASTIC: Note that the Demand constraint sets the variable V_Demand to be equal to supply.
    def Demand_Constraint ( M,  p, s, d, dem ):

        supply = sum(
          M.V_FlowOut[ p, s, d, S_i, S_t, S_v, dem]

          for S_t, S_v in M.helper_commodityUStreamProcess[ p, dem ]
          for S_i in M.helper_ProcessInputsByOutput[ p, S_t, S_v, dem ]
        )
        DemandConstraintErrorCheck( supply,  p, s, d, dem )
        expr = (supply == M.V_Demand[ p, s, d, dem])
        return expr
    
    #ELASTIC: Definition of V_Demand in terms of MinDemand and non-zero V_DemandSegment
    def DemandElasticity_Constraint(M,  p, s, d, dem):
        r"""\
    Defines the variable V_Demand as the sum of the MinDemand and non-zero V_DemandSegment
    variables.
    """
    
        expr = (M.V_Demand[ p, s, d, dem] == M.MaxDemand[ p, dem] * M.DemandSpecificDistribution[ s, d, dem] -
                sum([M.V_DemandSegment[ p, s, d, dem, z]
                for z in M.demand_segment]))
        return expr
    
    # ELASTIC: Bounds (size) of each V_DemandSegment variable
    def DemandSegment_bound(M,  p, s, d, dem):
        r"""\
        Defines the (0.0, upper bound) of each V_DemandSegment variable.
        """
        diff = ((value(M.MaxDemand[ p, dem]) - value(M.MinDemand[ p, dem])) * value(M.DemandSpecificDistribution[ s, d, dem])
                / value(M.num_demand_segments))
    
        return diff
    
    #Elastic
    def DemandSegment_bound_rule(M,  p, s, d, dem, z):
        r"""\
        Defines the (0.0, upper bound) of each V_DemandSegment variable.
        """
        diff = ((value(M.MaxDemand[ p, dem]) - value(M.MinDemand[ p, dem])) * value(M.DemandSpecificDistribution[ s, d, dem])
                / value(M.num_demand_segments))
    
        return (0.0, diff)
    
    # ELASTIC: Definition of Price from the price-demand elasticity curve.
    #Here price is independent of the demand variable which  makes me suspicios - Neha
    def PriceSegment_rule(M,  p, s, d, dem, z):
        r"""\
        Defines the price at each V_DemandSegment using the price-demand elasticity curve.
        """
        P0 = value(M.Price[ p, s, d, dem])
        D0 = value(M.Demand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem])
        minb = value(M.MinDemand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem])
        diff = (value(M.MaxDemand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem]) - minb) / value(M.num_demand_segments)
        D = minb + (z-0.5) * diff
        e = 1.0 / value(M.Elast[p, s, d, dem])
    
        P = (P0 * (D / D0) ** -e)#/(1 - e))
        return P
    
    # ELASTIC: Utility function that calculates the midpoint of each demand segment.
    # Note: this is only used in reporting and is not part of the model.
    def DemandSegment_midpoint_rule(M,  p, s, d, dem, z):

        minb = value(M.MinDemand[ p, dem]) * M.DemandSpecificDistribution[ s, d, dem]
        diff = (value(M.MaxDemand[ p, dem]) * M.DemandSpecificDistribution[ s, d, dem] - minb) / value(M.num_demand_segments)
        D = minb + (z - 0.5) * diff
        return D
    
    def Demand_rule(M,  p, s, d, dem):
        return value(M.Demand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem])

    def Demand_bounds(M,  p, s, d, dem):
        return (value(M.MinDemand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem]),
                value(M.MaxDemand[ p, dem]) * value(M.DemandSpecificDistribution[ s, d, dem]))

    M.del_component('TotalCost')
    M.del_component('DemandConstraint')
    M.del_component('M.DemandActivityConstraint_psdtv_dem_s0d0')
    M.del_component('DemandActivityConstraint')

    M.num_demand_segments      = Param()
    M.demand_segment           = Set(ordered=True, rule=lambda M: range(1, value(M.num_demand_segments) + 1))
    M.Elast                    = Param(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand)
    M.Price                    = Param(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand)
    M.MinDemand                = Param(M.time_optimize, M.commodity_demand)
    M.MaxDemand                = Param(M.time_optimize, M.commodity_demand)
    M.V_Demand                 = Var(M.DemandConstraint_rpsdc, initialize=Demand_rule,bounds=Demand_bounds)
    M.DemandConstraint_rpsdcz  = M.DemandConstraint_rpsdc * M.demand_segment
    M.DemandSegment_bound_value = Param(M.DemandConstraint_rpsdc, initialize=DemandSegment_bound)
    M.V_DemandSegment          = Var(M.DemandConstraint_rpsdcz,bounds=DemandSegment_bound_rule, initialize=0.0)
    M.PriceSegment             = Param(M.DemandConstraint_rpsdcz, initialize=PriceSegment_rule)
    M.DemandSegment_midpoint   = Param(M.DemandConstraint_rpsdcz, initialize=DemandSegment_midpoint_rule)
    M.DemandElasticityConstraint = Constraint(M.DemandConstraint_rpsdc, rule=DemandElasticity_Constraint)
    M.DemandConstraint         = Constraint( M.DemandConstraint_rpsdc, rule=Demand_Constraint)

    M.TotalWelfare             = Objective(rule=TotalWelfare_rule, sense=minimize)

    data = DataPortal(model = M)
    data.load(filename=dat)
    data.load(filename=dat1)
    instance = M.create_instance(data)
    return instance

def find_price(dm_instance, instance):
    time_fut        = dm_instance.time_future.keys()
    dV_Capacity     = dm_instance.V_Capacity.get_values() 
    alpha           = 0.4   #productivity of energy efficiency
    sigma           = 2     #elasticity of substitution
    P_theta         = 13.88 #marginal cost of energy efficiency
    eps             = -0.4  #demand elasticity
    PRICE_RANGE    = 0.99   # Max/MinDemand = (1 +/- PRICE_RANGE)* Demand
    DEMAND_SEGMENTS = 600    # number of steps
    beta           = 1.0    #efficiency credit
    #fix all new capacity to zero
    for i , j in sorted(instance.V_Capacity.keys()):
        if i in instance.tech_all.keys() and j in time_fut:
            instance.V_Capacity[i, j].fix(0)

    price_data = open("newPrice.dat", "w") #create a new price file
    print("""\
    data;
    param:     phi    MinESDemand:=
      # year   # season     # time     # demand   #phi   #minESDemand    
    """,file=price_data)
    for iaux in time_fut:
        Parameters = parameters(dm_instance, iaux, time_fut, instance, dV_Capacity, price_data, alpha, sigma, P_theta, eps, PRICE_RANGE)

    print("    ;\n",file=price_data)
    print("param num_demand_segments := %d ; # number of segments in the demand range" % DEMAND_SEGMENTS,file=price_data)
    print("param alpha := %f ; # productivity of energy efficiency" % alpha,file=price_data)
    print("param sigma := %f ; # elasticity of substitution" % sigma,file=price_data)
    print("param eps := %f ; # energy service demand elasticity" % eps,file=price_data)
    print("param efficiencyPrice := %f ; # energy service demand elasticity" % P_theta,file=price_data)
    print("param beta := %f ; # efficiency credit" % beta,file=price_data)
    sys.stdout.write('\a\a')
    sys.stdout.flush()
    price_data.close()

def temoa_efficiency(dat, dat2):
    M = temoa_create_model()
    def TotalWelfare_rule ( M ):
        actual_emissions = sum(
            M.V_FlowOut[ p, S_s, S_d, S_i, S_t, S_v, S_o]
          * M.EmissionActivity[ e, S_i, S_t, S_v, S_o]

          for  e, S_i, S_t, S_v, S_o in M.EmissionActivity.sparse_iterkeys()
          for S_s in M.time_season
          for S_d in M.time_of_day
         for p in M.time_optimize
         if M.ValidActivity( p, S_t, S_v )
         if e == 'co2')
    
        consumer_costs = sum(((M.ESDemand[ p, s, d, dem] - value(M.MinESDemand[ p, s, d, dem])) / value(M.num_demand_segments))* M.ESPriceSegment[ p, s, d, dem, z]
           for ( p, s, d, dem, z) in M.ESPriceSegment)

        producer_costs = sum( PeriodCost_rule(M,  p) for p in M.time_optimize )
        EEfficiency_cost = value(M.beta) * value(M.efficiencyPrice) * sum(M.efficiencyDemand[ S_p, S_s, S_d, S_c] for  S_p, S_s, S_d, S_c in M.DemandConstraint_rpsdc)

        return (producer_costs - consumer_costs + 0.1 *actual_emissions + EEfficiency_cost)

    def Demand_Constraint ( M,  p, s, d, dem ):
        supply = sum(
          M.V_FlowOut[ p, s, d, S_i, S_t, S_v, dem]

          for S_t, S_v in M.helper_commodityUStreamProcess[  p, dem ]
          for S_i in M.helper_ProcessInputsByOutput[  p, S_t, S_v, dem ]
        )
    
        DemandConstraintErrorCheck( supply,  p, s, d, dem )

        expr = (supply == M.elecDemand[ p, s, d, dem])

        return expr
    
    def efficiencyDemand_rule(M,  p, s, d, dem):
        phi = value(M.phi[ p, s, d, dem])
        PE = M.elecPrice[ p, s, d, dem]
        alpha = value(M.alpha)
        sigma = value(M.sigma)
        eps = value(M.eps)
        PT = value(M.efficiencyPrice)
        beta = value(M.beta)
        expr = (M.efficiencyDemand[p,s,d,dem] == phi * alpha **sigma * (beta * PT) **(-sigma) * (alpha**sigma * (beta * PT) ** (1-sigma) + (1-alpha)**sigma * PE **(1-sigma))**((eps+sigma)/(1-sigma)))
        return expr
    
    def elecDemand_rule(M,  p, s, d, dem):
        phi = value(M.phi[ p, s, d, dem])
        PE = M.elecPrice[ p, s, d, dem]
        alpha = value(M.alpha)
        sigma = value(M.sigma)
        eps = value(M.eps)
        PT = value(M.efficiencyPrice)
        beta = value(M.beta)
        expr = (M.elecDemand[p,s,d,dem] == phi * (1-alpha) **sigma * PE **(-sigma) * (alpha**sigma * (beta * PT) ** (1-sigma) + (1-alpha)**sigma * PE **(1-sigma))**((eps+sigma)/(1-sigma)))
        return expr
    
    def ESPrice_rule(M,  p, s, d, dem):
        PE = M.elecPrice[ p, s, d, dem]
        alpha = value(M.alpha)
        sigma = value(M.sigma)
        eps = value(M.eps)
        PT = value(M.efficiencyPrice)
        beta = value(M.beta)
        expr = (M.ESPrice[p,s,d,dem] == (alpha**sigma * (beta * PT) ** (1-sigma) + (1-alpha)**sigma * PE **(1-sigma))**(1/(1-sigma)))
        return expr
    
    def ESDemand_rule(M,p,s,d,dem):
        phi = value(M.phi[ p, s, d, dem])
        P = M.ESPrice[p,s,d,dem]
        eps = value(M.eps)
        expr = (M.ESDemand[p,s,d,dem] == phi * (P ** eps))
        return expr
    
    
    def ESPriceSegment_rule(M,  p, s, d, dem, z):
        """\
        Defines the price at each V_DemandSegment using the price-demand elasticity curve.
        """
        phi = value(M.phi[ p, s, d, dem])
        minb = value(M.MinESDemand[ p, s, d, dem])
        diff = (M.ESDemand[ p, s, d, dem] - minb) / value(M.num_demand_segments)
        D = minb + (z-0.5) * diff
        eps = value(M.eps)
        expr = (M.ESPriceSegment[p,s,d,dem,z] == (D/phi) ** (1/eps))
        return expr
    
    def consumer_cost_rule(M):
        expr = (0 <= sum(((M.ESDemand[ p, s, d, dem] - value(M.MinESDemand[ p, s, d, dem])) / value(M.num_demand_segments))* M.ESPriceSegment[ p, s, d, dem, z]
           for ( p, s, d, dem, z) in M.ESPriceSegment))
        return expr

    def real_obj(M): #STOCH ELASTIC
        a = sum( PeriodCost_rule(M, p) for p in M.time_optimize )
        expr = (a >= 0)
        return expr
        
    M.del_component('TotalCost')
    M.del_component('DemandConstraint')
    M.del_component('M.DemandActivityConstraint_psdtv_dem_s0d0')
    M.del_component('DemandActivityConstraint')
    # Efficiency: all the parameters
    M.num_demand_segments          = Param()
    M.demand_segment               = Set(ordered=True, rule=lambda M: range(1, value(M.num_demand_segments) + 1))
    M.elecPrice                    = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, domain=NonNegativeReals)
    M.phi                          = Param(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand)
    M.alpha                        = Param() 
    M.sigma                        = Param()
    M.eps                          = Param()
    M.beta                         = Param()
    M.efficiencyPrice              = Param() 
    M.efficiencyDemand             = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, domain=NonNegativeReals)
    M.elecDemand                   = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, domain=NonNegativeReals)
    M.ESPrice                      = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, domain=NonNegativeReals)
    M.ESDemand                     = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, domain=NonNegativeReals)
    M.MinESDemand                  = Param(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand)
    M.ESPriceSegment               = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, M.demand_segment, domain=NonNegativeReals)

    M.consumer_cost                = Constraint(rule=consumer_cost_rule)
    M.TotalCost = Constraint(rule=real_obj)
    M.efficiencyDemand_constraint  = Constraint(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, rule=efficiencyDemand_rule)
    M.elecDemand_constraint        = Constraint(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, rule=elecDemand_rule)
    M.ESPrice_constraint           = Constraint(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, rule=ESPrice_rule)
    M.ESDemand_constraint          = Constraint(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, rule=ESDemand_rule)
    M.ESPriceSegment_constraint    = Constraint(M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand, M.demand_segment, rule=ESPriceSegment_rule)
    M.DemandConstraint             = Constraint( M.DemandConstraint_rpsdc, rule=Demand_Constraint )

    M.TotalWelfare = Objective(rule=TotalWelfare_rule, sense=minimize)
    data1 = DataPortal(model = M)
    data1.load(filename=dat)
    data1.load(filename=dat2)
    instance = M.create_instance(data1)

    return instance

def efficiency_run():
    model = temoa_create_model()
    #dat = '/mnt/disk2/nspatank/Efficiency_nonlinear/data_files/US_National_ELC.dat'
    dat = 'D:/daniele_lerede/temoa-energysystem/data_files/Temoa_Europe.dat'
    dm_instance = solve_dm(model, dat)
    dat1 = 'D:/daniele_lerede/temoa-energysystem/temoa_model/price.dat'
    elastic_instance = temoa_elastic(dat, dat1)
    new_price = find_price(dm_instance, elastic_instance)

    dat2 = '/D/temoa/for_git/temoa/temoa_model/newPrice.dat'
    instance = temoa_efficiency(dat, dat2)
    optimizer = SolverFactory('ipopt')

    optimizer.options['max_iter'] = 10000
    results = optimizer.solve(instance, keepfiles=True, tee=True)

    instance.solutions.load_from(results)
    fp = open('results.csv', 'w')
    dm = open('demand.csv', 'w')
    print('\"', instance.name, '\"',file=fp)
    print('\"Model Documentation: ', instance.doc, '\"',file=fp)
    print('\"Solver Summary\"',file=fp)
    print('\"', results['Solver'][0], '\"',file=fp)
    # Objective
    print('\"Objective function is:', value(instance.TotalWelfare), '\"',file=fp)
    print('\"Total Cost is:', value(instance.TotalCost.body), '\"',file=fp)
    print('\"Consumer Cost is:', value(instance.consumer_cost.body), '\"',file=fp)
    for v in instance.component_objects(Var, active=True):
        varobject = getattr(instance, str(v))
        #IP()
        print("",file=fp)
        print("\"Variable: %s\", \"Notes: %s\"" % (v, varobject.doc),file=fp)
        print ("fixing"+str(v))
        for index in varobject:
            varobject[index].fixed = True
            print>>fp, "\"" + str(index) + "\"", varobject[index].value


    actual_emissions = sum(value(instance.V_FlowOut[ p, S_s, S_d, S_i, S_t, S_v, S_o]) * value(instance.EmissionActivity[ e, S_i, S_t, S_v, S_o])
    for  e, S_i, S_t, S_v, S_o in instance.EmissionActivity.sparse_iterkeys()
    for S_s in instance.time_season.keys()
    for S_d in instance.time_of_day.keys()
    for p in instance.time_optimize.keys()
    if instance.ValidActivity( p, S_t, S_v )
    if e == 'co2')
    print("year season time demand elecDemand elecPrice ESDemand ESPrice efficiencyDemand CO2_emissions",file=dm)
    for p, s, d, dem  in sorted(instance.DemandConstraint_rpsdc.keys()):
        key = p, s, d, dem
        #IP()
        print >> dm,p,s,d,dem, value(instance.elecDemand[key]), value(instance.elecPrice[key]), \
                value(instance.ESDemand[key]), value(instance.ESPrice[key]), \
                value(instance.efficiencyDemand [key]), sum(value(instance.V_FlowOut[ p, s, d, S_i, S_t, S_v, S_o]) * value(instance.EmissionActivity[ e, S_i, S_t, S_v, S_o])
    for  e, S_i, S_t, S_v, S_o in instance.EmissionActivity.sparse_iterkeys()
    if instance.ValidActivity( p, S_t, S_v )
    if e == 'co2')

if __name__ == "__main__":
    efficiency_run()
    sys.stdout.write('\a\a')
    sys.stdout.flush()
