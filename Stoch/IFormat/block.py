#Export
__all__=('Block')

#Import
from   sets               import Set
from   numpy              import float64
from smps_python.Stoch.Scenarios import dScen
from smps_python.Stoch.Cases     import dCase as dc 

#------------------------------------
#Block section analyser
#------------------------------------
def Block(b_list, Root): 

    """ 
    Block section analysier
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
    for u in b_list:       

        #Case (1): New scenario
        if u[0]=='BL':
            s=dScen()   #New dscenario
            name=u[1]   #Block name
            per= u[2]   #Time stage

            #Scenario parameters
            s.set_stages(Stages)
            s.set_delimiters(delt['RHS'],delt['RANGES'],\
                             delt['BOUNDS'])
            s.set_time(per)
            
            #Verification (1): Numeric probablility
            try:
                pro=float64(u[3])
            except:
                raise NameError('Block probability needs to be numeric')

            #Case (1.1): Current realization evaluation
            if name==cr:

                #Verification (2): Equal period
                if per <>ct:
                    raise NameError("Realizations cannot be located at multiple stages")

                else:
                    r_count+=1
                    s.add_coordinate(name,r_count,per,pro)
                    CL.add_scenario(s)

            #Case (1.2): New realization
            else:

                #Verification (3): Non repeated realization
                if name in rea:
                    raise NameError('.Sto realizations are not organized properly')

                #Verification (4): Time in .tim file
                elif per not in Stages:
                    raise NameError('Stage '+per+' is not declared at the .tim file')

                #Verification (5): Time order
                elif Stages.index(per)<st:
                    raise NameError('.sto BLOCKS section does not follow the .tim stage order')

                else:                    
                    cr=str(name)         #Name update
                    st=Stages.index(per) #Stage counter update 
                    ct=per               #Current stage name
                    rea.add(name)        #Realization update
                    r_count=1            #Realization count

                    #Scenario update
                    s.add_coordinate(name,r_count,per, float64(pro))
                    
                    #New stocase
                    CL=dc.dStoCase(Stages)
                    CL.add_scenario(s)

                    #New entry
                    L.append(CL)            

                    
        #Case (2): New scenario
        else:

            #Case (2.1) Bound type parameters
            if u[1]==delt['BOUNDS']:

                #Verification (6): Bound vector length
                if len(u) <> 4:
                    raise NameError(".sto BLOCKS section must have 4 entries per line\n"
                             + "(1) Bound type\n" \
                             + "(2) Bound vector name\n"\
                             + "(3) Variable name \n" \
                             + "(4) Realization value \n")
                else:
                    try:
                        s.add_realization(u[3],u[0:3])    #Add new realizations
                    except:
                        raise NameError("Bound "+u[0:3]+" cannot be processed")

            #Case (2.2) Block, RHS, RANGES
            else:

                #Verification (7): Vector length
                if len(u)%2<>1 or len(u)<3:
                    raise  NameError('.sto BLOCK coefficients are incomplete')
                else:
                    cons=(len(u)-1)/2   #Number of entries per line
                    
                    for j in range(0,cons):
                        s.add_realization(u[2*j+2],[u[0], u[2*j+1]])

    #------------------------
    #Last verification
    #------------------------
    for u in L:
        u.verification(Root) #Base cases verification
    
    return dc.Cartesian(L)
          

