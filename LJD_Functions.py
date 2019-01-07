
# coding: utf-8

# In[ ]:
# LJD_Functions.py
# Purpose: To contain all cobra functions that I use regularly such that I can import them into whatever main script I am using 
# Functions contained in this script:
    # changeMedia_PA_LJD - changes the media conditions of a cobrapy model

# import packages
from copy import *

# changeMedia_PA_LJD adapted from the Matlab function with the same name
    # Changes the media condition of the model by altering the bounds of the appropriate exchange reactions
    # Inputs:
        # model: a cobrapy model
        # media: the media condition to change the environment to
            # 1 - LB media
            # 2 - SCFM
            # 3 - Minimal media
        # limEX: a list of exchanges ('EX_cpd#####(e)') that are added as limited exchanges to minimal media
    # Outputs:
        # modelOutput: a cobrapy model in the new media condition (with adjusted exchanges)
def changeMedia_PA_LJD(model, media, limEX=[]):
    modelOutput = deepcopy(model)
    
    # LB Components:
    # Metabolites that are in excess in LB
    LB_open_exchanges = ['EX_cpd00001_e', 
                     'EX_cpd00009_e',
                     'EX_cpd00011_e',
                     'EX_cpd00021_e',
                     'EX_cpd00034_e',
                     'EX_cpd00048_e',
                     'EX_cpd00058_e',
                     'EX_cpd00205_e',
                     'EX_cpd00254_e',
                     'EX_cpd00971_e',
                     'EX_cpd01012_e',
                     'EX_cpd00067_e']
    
    # Metabolites that are more limited but available in LB
    LB_limited_exchanges = ['EX_cpd00023_e',
                            'EX_cpd00027_e',
                            'EX_cpd00033_e',
                            'EX_cpd00035_e',
                            'EX_cpd00039_e',
                            'EX_cpd00041_e',
                            'EX_cpd00051_e',    
                            'EX_cpd00054_e',    
                            'EX_cpd00060_e',    
                            'EX_cpd00065_e',    
                            'EX_cpd00066_e',    
                            'EX_cpd00069_e',    
                            'EX_cpd00084_e',    
                            'EX_cpd00107_e',    
                            'EX_cpd00119_e',    
                            'EX_cpd00129_e',    
                            'EX_cpd00156_e',    
                            'EX_cpd00161_e',    
                            'EX_cpd00305_e',   
                            'EX_cpd00322_e',    
                            'EX_cpd00092_e',    
                            'EX_cpd00307_e',
                            'EX_cpd03091_e']
    
    # SCFM Components:
    SCFM_open_exchanges = ['EX_cpd00001_e',
                           'EX_cpd00009_e',
                           'EX_cpd00011_e',
                           'EX_cpd00021_e',
                           'EX_cpd00023_e',
                           'EX_cpd00027_e',
                           'EX_cpd00033_e',
                           'EX_cpd00035_e',    
                           'EX_cpd00039_e',   
                           'EX_cpd00041_e',    
                           'EX_cpd00048_e',    
                           'EX_cpd00051_e',   
                           'EX_cpd00054_e',   
                           'EX_cpd00060_e',    
                           'EX_cpd00064_e',   
                           'EX_cpd00065_e',    
                           'EX_cpd00066_e',    
                           'EX_cpd00067_e',    
                           'EX_cpd00069_e',   
                           'EX_cpd00084_e',    
                           'EX_cpd00107_e',    
                           'EX_cpd00119_e',    
                           'EX_cpd00129_e',    
                           'EX_cpd00156_e',    
                           'EX_cpd00221_e',   
                           'EX_cpd00161_e',   
                           'EX_cpd00205_e',   
                           'EX_cpd00209_e',    
                           'EX_cpd00254_e',   
                           'EX_cpd00322_e',    
                           'EX_cpd00971_e',    
                           'EX_cpd00013_e']
    
    # Minimal Media Components: 
    minimalMedia_open_exchanges = ['EX_cpd00001_e', 
                                   'EX_cpd00009_e', 
                                   'EX_cpd00011_e',
                                   'EX_cpd00021_e',
                                   'EX_cpd00030_e',
                                   'EX_cpd00034_e',
                                   'EX_cpd00048_e',
                                   'EX_cpd00058_e',
                                   'EX_cpd00067_e',
                                   'EX_cpd00149_e',
                                   'EX_cpd00205_e',
                                   'EX_cpd00254_e',
                                   'EX_cpd00528_e',
                                   'EX_cpd00971_e', 
                                   'EX_cpd00013_e', 
                                   'EX_cpd01012_e', 
                                   'EX_cpd10516_e',
                                   'EX_cpd00244_e']
   
    # Set the new media conditions
    for ex in modelOutput.exchanges:
        ex.upper_bound = 1000
        ex.lower_bound = 0
    # Set aerobic exchange (O2) to 20 mmol/gDW/hr 
    modelOutput.reactions.EX_cpd00007_e.lower_bound = -20
    
        # Media == 1 Change bounds to LB
    if media == 1:
        # Set open lb exchanges to -1000
        for ex_LB in modelOutput.reactions:
            if ex_LB.id in LB_open_exchanges:
                ex_LB.lower_bound = -1000
            elif ex_LB.id in LB_limited_exchanges:
                ex_LB.lower_bound = -10
        
    # Media == 2 Change bounds to SCFM
    elif media == 2:
        for ex_SCFM in modelOutput.reactions:
            if ex_SCFM.id in SCFM_open_exchanges:
                ex_SCFM.lower_bound = -10 #According to the matlab script...
        
    # Media == 3 Change bounds to minimal + exchanges?
    elif media == 3:
        for ex_minimal in modelOutput.reactions:
            if ex_minimal.id in minimalMedia_open_exchanges:
                ex_minimal.lower_bound = -1000
        if len(limEX) > 0:
            for ex_minimal_lim in modelOutput.reactions:
                if ex_minimal_lim.id in limEX:
                    ex_minimal_lim.lower_bound = -10
        
    elif media == 0:
        modelOutput.reactions.EX_cpd00007_e.lower_bound = 0
        print('all exchange bounds set to [0,1000]')
            
    else:
        print('unrecognized media condition. Please enter 1 for LB; 2 for SCFM; 3 for minimal media')
   
    return(modelOutput) 

