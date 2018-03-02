
#Export
__all__=('ScenModifier')

def Rhs(model,root,rhs):
    """ 
    Model rhs modification
    rhs= scenario rhs modifications
    """
    
    for u in rhs: 

        try :
            model.b[u]=rhs[u]
        except:
            raise NameError('Constraint ' +u+' does not belong'\
                            +' the model constraints')
 

#-------------------------------------------
#Root scenario modification
#-------------------------------------------
def ScenModifier(model, root, scen):

    """
    Scenario modification

    Model: Pyomo root concrete model
    Root : DataModel  Object
    scen : Scenario   Object
    """

    # Pyomo param
    bl=  scen.realizations['BL']
    rhs= scen.realizations['RHS']
    ran= scen.realizations['RANGES']
    
    #RHS modification
    Rhs(model,root,rhs)
    
    
