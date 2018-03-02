#Export
__all__=('DeModel', 'ModelInstance')

#import
from smps_python.DeModel import DataModel
from pyomo.core   import *

def DeModel(data):

    """ 
    Builds scenario  linear stochastic problem 
    from data model
    """
    #--------------------------------------------
    #Pyomo model
    #--------------------------------------------
    m=ConcreteModel()     #Pyomo concrete model

    #--------------------------------------------
    #Sets
    #--------------------------------------------
    m.Var=Set( initialize=data.variables)              #Model variables 
    m.Cons=Set( initialize=data.constraints)           #Model constraints
    m.Stages=Set(initialize=data.stages, ordered=True) #Model time stages
    m.Ranges=Set(initialize=data.ranges_constraints()) #Range equations
    
    #--------------------------------------------
    #Parameters
    #--------------------------------------------
    typ=data.constraint_type #Constraint clasification
    m.obname= typ['N'][0]   #Objetive name   
        
    #Constaraint coefficients----------------------------------    
    m.A=Param(m.Cons, m.Var, initialize=data.matrix,\
              default=0, mutable=True)

    #Constraint  Right-Hand-Side Coefficients
    m.b=Param(m.Cons, initialize=data.rhs, \
              default=0, mutable=True)

    #Ranges parameters
    m.rang=Param(m.Ranges, initialize=data.ranges_coefficients(),\
                 default=0, mutable=True)

    #Objective cost
    def cost_rule(m,i):
        return m.A[ m.obname,i].value
    m.cost=Param(m.Var, rule=cost_rule, \
                 default=0, mutable=True)
    
    #--------------------------------------------
    #Variables
    #--------------------------------------------

    #Default variables: Continuous positive
    m.x=Var(m.Var, bounds=(0,None))
    m.SC=Var(m.Stages)
    
    #Domain alteration (Free, Positive, Negative Behavior)
    for i in data.free_variables():           #Free variables
        m.x[i].free()
    for i in data.negative_variables():  #Negative variables
        m.x[i].domain=NegativeReals 

    #Variable bounds (Upper, Lower, Upper Integer, Fixed)
    up=data.upbound()          #Upper bound
    lo=data.lobound()          #Lower bound
    ui=data.uibound()          #UI bound
    fx=data.fixed_variables()  #Fixed variables
    
    for i in up:
        m.x[i].setub(up[i])
    for i in lo:
        m.x[i].setlo(lo[i])
    for i in ui:
        m.x[i].setub(ui[i])
    for i in fx:
        m.x[i].fix(fx[i]) 

    #Variable nature (Integer, Binary)
    for i in data.integer_variables:   #Integer variables
        m.x[i].domain=Integers

    for i in data.binary_variables():  #Binary variables
        m.x[i].domain=Binary

    #------------------------------------------------
    #Constraints
    #-----------------------------------------------   
       
    #Model constraints
    def ConsRule(m,i):

        # Ax<=b constraints
        if i in typ['L']:
            if i in m.Ranges:   #Range type
                return (m.b[i]-abs(m.rang[i]), sum(m.A[i,j]*m.x[j] for j in m.Var), m.b[i])
            else:
                return sum(m.A[i,j]*m.x[j] for j in m.Var)<=m.b[i]

        #Ax>=b constaints
        elif i in typ['G']:
            if i in m.Ranges:   #Range type
                return (m.b[i], sum(m.A[i,j]*m.x[j] for j in m.Var), m.b[i]+abs(m.rang[i]) )
            else:
                return sum(m.A[i,j]*m.x[j] for j in m.Var)>=m.b[i]

        #Ax=b constarints
        elif i in typ['E']:
            if i in m.Ranges:    #Range type
                if m.ran[i]>0:
                    return (m.b[i], sum(m.A[i,j]*m.x[j] for j in m.Var), m.b[i]+m.rang[i])
                else:
                    return (m.b[i]+m.rang[i], sum(m.A[i,j]*m.x[j] for j in m.Var), m.b[i])
            else:
                return sum(m.A[i,j]*m.x[j] for j in m.Var)==m.b[i]

        #Objetive function 
        else:
            return Constraint.Skip

    #Constraint attribute
    m.ConsRule=Constraint(m.Cons, rule=ConsRule)

    #----------------------------------------------
    #Objective Definition
    #----------------------------------------------
    st2var=data.st_to_var #Stage to var structure
    m._st2var=st2var      #Model asignation
    
    #Stage cost definition
    def Stage_Cost(m,i):
        return m.SC[i]==\
            sum(m.cost[j]*m.x[j]\
                for j in m.Var if i==st2var[j])
    m.Stage_Cost=Constraint(m.Stages, rule=Stage_Cost)
    
    #Scenario objective definition
    def Obj_rule(m):
        return sum(m.SC[i] for i in m.Stages)
    m.obj=Objective(rule=Obj_rule)

    #-------------------------------------------- 
    #Model return
    #--------------------------------------------
    return m
       
#------------------------------------------------
# Model modification
#------------------------------------------------
def ModelInstance(Root,scen):
    """
    Deterministic model instance modification
    m: Pyomo deterministic model Object
    scen: Scenario objetc
    """
    
    #New pyomo model
    m=Root.clone()
    rea=scen.realizations    #Scenario verified realizations

    #-------------------------------
    #Block modifications
    #-------------------------------
    for u in rea['BL']:
        
        if u[0]<>m.obname:
            m.A[u].value=rea['BL'][u] #Constraint coeffcients
        else:
            m.cost[u[1]].value=rea['BL'][u]
    #-------------------------------
    #Rhs modifications
    #-------------------------------
    for u in rea['RHS']:
        m.b[u].value=rea['RHS'][u]

    #-------------------------------
    #Range modifications
    #------------------------------
    for u in rea['RANGES']:
        m.rang[u].value=rea['RANGES'][u]

    #------------------------------
    #Bound modifications
    #------------------------------

    for i in rea['UP']:
        m.x[i].setub(rea['UP'][i]) #UP bound
    for i in rea['LO']:
        m.x[i].setlo(rea['LO'][i]) #LO bound  
    for i in rea['UI']:
        m.x[i].setub(rea['UI'][i]) #UI bound
    for i in rea['FX']:
        m.x[i].fix(rea['FX'][i])   #Fixed variable 

    
    return m
    
