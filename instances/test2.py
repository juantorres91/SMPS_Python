from smps_python import (DataModel, StoModel, DeModel, ModelInstance)

cor_file="sslp_5_25-50.cor"
sto_file="sslp_5_25-50.sto"
tim_file="sslp_5_25-50.tim"

#Root model
Root=DataModel(cor_file, tim_file)

#Stochastic case
Case=StoModel(Root, sto_file)

#Pyomo model
model=DeModel(Root)

#------------------------------------------
#Stochastic structure
#------------------------------------------

def pysp_scenario_tree_model_callback():
    from pyomo.pysp.scenariotree.tree_structure_model import \
         CreateAbstractScenarioTreeModel

    #Model
    st_model=CreateAbstractScenarioTreeModel()

    #----------------------------------------
    #Basic Spectification
    #----------------------------------------

    #Stages-------------------
    for i in Root.stages:
        st_model.Stages.add(i)

    #Nodes--------------------
    for i in sorted (Case.tree.nodes()):
        st_model.Nodes.add(i)

    #Scenarios----------------
    for i in sorted(Case.names):
        st_model.Scenarios.add(i)

    st_model=st_model.create_instance()

    #----------------------------------------
    #Advanced Spectification
    #----------------------------------------

    #Scenario Leaf Node
    for i in sorted(Case.names):
        st_model.ScenarioLeafNode[i]=Case.scenario_node[i]

    #Node attributes
    for i in st_model.Nodes:
        #Conditional probability 
        st_model.ConditionalProbability[i]=Case.tree.node[i]['probability']

        #Stage
        st_model.NodeStage[i]=Case.tree.node[i]['stage']

        #Children Node
        for j in Case.tree.edges(i):
            st_model.Children[i].add(j[1])

    #-------------------------------------------
    #Variable /Objective Spectification
    #-------------------------------------------
    for i in Root.variables:
        st_model.StageVariables[Root.st_to_var[i]].add('x['+i+']')

    for i in Root.stages:
        st_model.StageCost[i]='SC['+i+']'
        
    return st_model

def pysp_instance_creation_callback(scenario_name, node_names):

    scenario=Case.scenario(scenario_name)
    instance=ModelInstance(model,scenario)
    return instance

  
    
