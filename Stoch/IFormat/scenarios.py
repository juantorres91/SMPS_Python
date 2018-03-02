#Export
__all__=('Scenarios')

#Import
from sets       import Set 
from numpy      import float64
from networkx   import DiGraph
from SMPS.Stoch.TreeUtils import (StoTree,tree_exploration)
from SMPS.Stoch.Scenarios import Scen
from SMPS.Stoch.Cases     import StoCase

#----------------------------------------
#Scenario storing  and clasification
#---------------------------------------
def Scenarios(s_list,Root,Edge=False):

    """
    Scenario section analyser
    Root: Deterministic data model
    """
    #Sto parameters
    SC=StoCase()   #Stochastic List
    G=DiGraph()    #Stochastic realization tree
    sc=Set()       #Scenario set
    pro={}         #Scenario probability
    delt=Root.delimiters() #Vector Name delimiters

    #Time parameters
    Stages=Root.stages     #Ordered time set
    st= Set(Stages)

    #-----------------------------------------------
    #Gathering information:
    #-----------------------------------------------
    for u in s_list:
        
        #-------------------------------------------
        #Case (1): Scenario delimiter
        #-------------------------------------------
        if u[0]=='SC':
            #Parameters
            tim=u[-1]  #Separation time

            #Verification (1): time in .tim
            if tim not in st:
                raise NameError('Stage '+ tim+'is not defined at '\
                                +'the .tim file')

            #Verification (2): Numeric probability
            try:
                pr=float64(u[3])
            except:
                raise NameError('Scenario probability needs to be numeric')
                
            G.add_edge(u[2],u[1],time=tim) #Scenario path 
            pro[u[1]]=pr                   #Scenario probability 

            #Verification (3): Non previous scenario 
            if u[1] in sc:
                raise NameError('Scenario '+u[1]+' has been already defined')                      
            else:
                sc.add(u[1])                      #New scenario in list
                s=Scen()                          #New scenario object
                s.set_delimiters(delt['RHS'],delt['RANGES'],\
                             delt['BOUNDS'])  #Set scenario delimiters
                SC.set_node_reference(u[1],u[1]+'_'+Stages[-1])#Scenario to node reference
                SC.add_scenario(s,distrib=False,name=u[1] )    #Scenario in list
              

        #----------------------------------------------
        #Case (2): New scenario
        #----------------------------------------------
        else:
            #Case (2.1) Bound type parameters
            if u[1]==delt['BOUNDS'] :

                #Verification (4): Bound vector length
                if len(u) <> 4:
                    raise NameError(".sto SCENARIOS section must have 4 entries per line\n"
                             + "(1) Bound type\n" \
                             + "(2) Bound vector name\n"\
                             + "(3) Variable name \n" \
                             + "(4) Realization value \n")
                else:
                    try:
                        s.add_realization(u[3],u[0:3]) #Add new realizations
                    except:
                        raise NameError("Bound "+u[0:3]+" cannot be processed") 
                        
            #Case (2.2) Block, RHS, RANGES
            else:

                #Verification (5): Vector length
                if len(u)%2<>1 or len(u)<3:
                    raise  NameError('.sto SCENARIOS coefficients are incomplete')
                else:
                    cons=(len(u)-1)/2   #Number of entries per line
                    
                    for j in range(0,cons):
                        s.add_realization(u[2*j+2],[u[0], u[2*j+1]])

    #---------------------------------
    #List verification
    #---------------------------------
    SC.verification(Root)
    
    #---------------------------------
    #Tree generation and verification
    #---------------------------------
    SC.set_stochastic_tree( StoTree(G,sc,Stages,pro,Edge))

    #---------------------------------
    #Scenario analysis-Scenario derivation
    #---------------------------------
    tree_exploration(SC.reference, G)
    
    #Return  
    return SC

    

