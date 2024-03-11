# ETL

from temoa_initialize import *
from pyomo.core import value
from pyomo.environ import *

# expr = C1
# C0[r,t]*V_CapIncrease(M,r,p,t)**-bLR == M.V_CostInvest[r,t,p]

def V_CapIncrease(M, r, t, p):
    timesteps = list(j for j in M.time_optimize)
    timesteps = timesteps[:timesteps.index(p) + 1]

    cumCAP_EX = 0
    for i in range(0, len(timesteps)):
        try:
            proof = value(M.V_NewCapacity[r, t, timesteps[i]])
        except KeyError: #KeyError in M.V_NewCapacity some time (not existing in first years)
            proof = None
        if proof:
            if value(M.V_NewCapacity[r, t, timesteps[i]]) != 0:
                cumCAP_EX = value(M.V_NewCapacity[r, t, timesteps[i]])
                break

    if cumCAP_EX == 0:  # if still zero, because no Capacity is present in that years
        x = 0
    else:
        V_Cap = list()
        for i in range(0, len(timesteps)):
            try:
                V_Cap.append(value(M.V_NewCapacity[r, t, timesteps[i]]))
            except KeyError:
                V_Cap.append(0)

        x = sum(V_Cap) / cumCAP_EX
    return x

def InitialCost(M,r,t):
    pp = list(j for j in M.time_optimize)
    pp = pp[pp.index(2020):] #consider technology learning only from 2020, since before costs should follow historical
    #trends
    for i in range(0, len(pp)):
        try:
            C0 = M.CostInvest[r, t, pp[i]]
            if C0 != 0:
                break
        except KeyError:
            continue
    return C0

def V_CostInvest(M, r, t, p):

    if p <= 2020:

        return M.CostInvest[r, t, p] #follow historical trends until 2020

    else:

        LRtest = 0

        try:
            LR = M.LearningRate[r, t]
        except KeyError:
            LR = 0

        if LR == -1 or LR == 0:
            LRtest = None
        else:
            pass

        if LRtest == None:

            return M.CostInvest[r, t, p]

        if value(V_CapIncrease(M, r, t, p)) != 0:

            from math import log2 as log2
            C0 = InitialCost(M, r, t)
            V_CostInvest = C0 * V_CapIncrease(M, r, t, p)**-log2(1 / (1 - LR))

            return V_CostInvest

        else:

            timesteps = list(j for j in M.time_optimize)
            timesteps = timesteps[:timesteps.index(p)+1]
            for i in range(0, len(timesteps)):
                try:
                    proof = value(M.CostInvest[r, t, timesteps[i]])
                except KeyError:
                    proof = None
                if proof != None:
                    V_CostInvest = value(M.CostInvest[r, t, timesteps[i]])
                    break

            try:
                return V_CostInvest
            except UnboundLocalError:
                print('\nUnbondLocalError for tech: {} and p: {}\n'.format(t, p))

def search_string_pattern(pattern,position,string):
    if position + len(pattern) <= len(string):
        substring = string[position : position + len(pattern)]

        if substring == pattern:
            return string

    #patterns = ['EXS']
  #for pattern in patterns:

def LearningIndexes(M):
    indexes = set()
    for (r,p,t,v) in M.processLoans:
        if search_string_pattern('ELC', 0, t):
            if (not search_string_pattern('EXS', len(t)-3, t)) and (not search_string_pattern('FT', 4, t)) and \
                    (not search_string_pattern('LNK', len(t)-3, t)):
                indexes.add((r, t))
        if search_string_pattern('HH2', 0, t):
            if (not search_string_pattern('FT', 4, t)) and (not search_string_pattern('LNK', len(t)-7, t)) and \
                    (not search_string_pattern('STG', 4, t)) and (not search_string_pattern('DEL', 4, t)) and  \
                    (not search_string_pattern('WE_DEL', 4, t)) and (not search_string_pattern('WE_DMY', 4, t)) \
                    and (not search_string_pattern('BLD', 4, t)):
                indexes.add((r, t))
        if search_string_pattern('TRA_ROA_CAR', 0, t):
            if (not search_string_pattern('EXS', len(t)-3, t)):
                indexes.add((r, t))
    return indexes

def CostInvestIndexes(M):
    indexes = set()
    for (r,p,t,v) in M.processLoans:
        if search_string_pattern('ELC', 0, t):
            if (not search_string_pattern('EXS', len(t) - 3, t)) and (not search_string_pattern('FT', 4, t)) and \
                    (not search_string_pattern('LNK', len(t) - 3, t)) and (not search_string_pattern('BLD', 4, t)):
                indexes.add((r, t, p))
        if search_string_pattern('HH2', 0, t):
            if (not search_string_pattern('FT', 4, t)) and (not search_string_pattern('LNK', len(t)-7, t)) and \
                    (not search_string_pattern('STG', 4, t)) and (not search_string_pattern('DEL', 4, t)) and  \
                    (not search_string_pattern('WE_DEL', 4, t)) and (not search_string_pattern('WE_DMY', 4, t)) \
                    and (not search_string_pattern('BLD', 4, t)):
                indexes.add((r, t, p))
        if search_string_pattern('TRA_ROA_CAR', 0, t):
            if (not search_string_pattern('EXS', len(t) - 3, t)):
                indexes.add((r, t, p))
    return indexes