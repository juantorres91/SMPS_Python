#Export 
__all__=('Indep')

#Import 
from   sets               import Set
from   numpy              import float64
from smps_python.Stoch.Scenarios import dScen
from smps_python.Stoch.Cases     import dCase as dc             

#------------------------------------
#Independent section analyser
#------------------------------------
def Indep(i_list, Root):

    """ 
    Indep section analysier
    Root: Deterministic DataModel
    """

    #Sto parameters:
    L=[]                   #List of scenario cases
    rea=Set()              #Set of indexed realizations
    cr=''                  #Current realization
    r_count=0              #Number of scenarios per realization
    delt=Root.delimiters() #Vector Name delimiters
        
    #Tim parameters
    st=0           #Current time stage
    ct=''          #Current time stage name
    Stages=Root.stages     #Ordered time set
    
    #Gathering infortmation
    for  u in i_list:       

        #Scenario parameters
        s=dScen()      #New dScenario
        pro=u[-1]      #Scenario probability
        per=u[-2]      #Senario stage
        val=u[-3]      #Realization value
        name=u[0:-3]   #Realization name

        s.set_stages(Stages)                  #Update new scenario time
        s.set_delimiters(delt['RHS'],delt['RANGES'],\
                             delt['BOUNDS'])  #Set scenario delimiters       
        s.set_time(per)                       #Set verification time
        s.add_realization(val,name)           #Update realization
        
        #Case (1): Current realization  evaluation
        if str(name)==cr:

            #Verification (1): Equal period
            if per <>ct:
                raise NameError("Realizations cannot be located at multiple stages")
            else :
                r_count+=1
                s.add_coordinate(name,r_count,per, float64(pro))
                CL.add_scenario(s)
                
        #Case (2): New realization
        else:

            #Verification (2): Non repeated realization
            if str(name) in rea:
                raise NameError('.Sto realizations are not organized  properly')

            #Verification (3): Time in .tim file
            elif per not in Stages:
                raise NameError('Stage '+per+' is not declared at the .tim file')

            #Verification (4): Time order
            elif Stages.index(per)<st:
                raise NameError('.sto INDEP section does not follow the .tim stage order')

            else:
                cr=str(name)         #Name update
                st=Stages.index(per) #Stage counter update 
                ct=per               #Current stage name
                rea.add(str(name))   #Realization colection update
                r_count=1            #Update realization count

                #Scenario update
                s.add_coordinate(name,r_count,per, float64(pro))
                
                #New stocase
                CL=dc.dStoCase(Stages)
                CL.add_scenario(s)

                #New entry
                L.append(CL)

    #------------------------
    #Last verification
    #------------------------
    for u in L:
        u.verification(Root) #Base cases verification

    #Return
    return dc.Cartesian(L)

                
                
        

        
