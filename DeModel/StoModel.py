from pyomo.environ  import* 
from SMPS.Structure import DeModel 
from SMPS.Stoch     import StoList



def Det_Model(corfile, timfile): 
    #Model
    Model=DeModel(corfile,timfile) 
    m=ConcreteModel()

    OB_N=''              #Objetive Name
    for i in Model.eq:
        if Model.eq[i]=='OBJ':
            OB_N=i

    #------------------------------------------------------------       
    #Sets
    #------------------------------------------------------------
    m.Cont=Set(initialize=Model.c_var)  #Continuos Variable set
    m.Int= Set(initialize=Model.i_var)  #Integer Variable set
    m.Var= m.Cont | m.Int               #Variable set
    
    m.Cons=Set(initialize=Model.eq.keys())     #Constraint Set

    m.Time=RangeSet(0, max(Model.TS.values())) #Stages Set

    #-----------------------------------------------------------
    #Parameters
    #-----------------------------------------------------------
    m.A=Param(m.Cons, m.Var, initialize=Model.M, default=0) #Matrix coefficients
    m.b=Param(m.Cons, initialize=Model.rhs, default=0)      #Rhs vector

    #-----------------------------------------------------------
    #Variables
    #_----------------------------------------------------------
    m.x=Var(m.Var, bounds=(0,float('inf')))         #Model Variables- Default Non-Negative Reals
    m.SV=Var(m.Time)                              #Stage Cost
    #Domain restiction
    for i in m.Var:
        if i in Model.fr:   #Free variables
            m.x[i].setlb(- float('inf'))
            m.x[i].setup( float('inf'))
        elif i in Model.mi: #Negative variables
            m.x[i].setup(0)
            m.x[i].setlb(-float('inf'))

    for j in Model.fx.keys(): #Fixed variables
            m.x[j].fix(Model.fx[j])

    for j in Model.up.keys(): #Upper bound
            m.x[j].setub(Model.up[j])
            
    for j in Model.ui.keys(): #Upper Integer bound
            m.x[j].setub(Model.ui[j])
            
    for j in Model.lo.keys(): #Lower bound
            m.x[j].setlb(Model.lb[j])
    
    #Variable nature

    for i in m.Int:                               #Integer Variables
        m.x[i].domain=Integers

    for j in Model.bv:                            #Binary VAriables 
            m.x[j].domain=Binary
    
    
    #Constraints 
    def ConsRule(m,i):                            #Constraint rules
        if Model.eq[i]=='L':
            return sum(m.A[i,j]*m.x[j] for j in m.Var)<=m.b[i]
        elif Model.eq[i]=='G':
            return sum(m.A[i,j]*m.x[j] for j in m.Var)>=m.b[i]
        elif Model.eq[i]=='E':
            return sum(m.A[i,j]*m.x[j] for j in m.Var)==m.b[i]
        else:
            return Constraint.Skip
    m.ConsRule=Constraint(m.Cons, rule=ConsRule)

    #Objective Definition
    
    def Stage_Cost(m,i):
        return m.SV[i]==sum(m.A[OB_N,j]*m.x[j] for j in m.Var if Model.TS[j]==i)
    m.Stage_Cost=Constraint(m.Time, rule=Stage_Cost)

    return m

def pysp_scenario_tree_model_callback():

    scenarios=len(ScData)
    from pyomo.pysp.scenariotree.tree_structure_model \
        import CreateConcreteTwoStageScenarioTreeModel

    st_model = CreateConcreteTwoStageScenarioTreeModel(scenarios)

    first_stage = st_model.Stages.first()
    second_stage = st_model.Stages.last()

    # First Stage definitions
    st_model.StageCost[first_stage] = 'SV[0]'
    st_model.StageCost[second_stage]= 'SS[1]'

    #Stage Variables
    for i in t1:         #First stage variable
        st_model.StageVariables[first_stage].add('x['+str(i)+']')

    for i in t2:         #Second stage variable
        st_model.StageVariables[second_stage].add('x['+str(i)+']')
    
    #Scenario Probability
    st_model.ConditionalProbability['RootNode']=1

    for i in range(0, len(ScData)):
        st_model.ConditionalProbability['LeafNode_Scenario'+str(i+1)]=Pro[i]

    return st_model








if __name__=="__main__":
    import sys
    Model=Det_Model(sys.argv[1], sys.argv[2])
    Model.pprint()
   # for i in Model.Var:
        #print i, Model.x[i].is_integer()
