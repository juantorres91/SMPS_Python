#Export
__all__=('StoModel')

#Import 
from IFormat      import (Block, Scenarios, Indep)
from StoFile      import Sto_Section

def StoModel(Root,sto_file,Edge=False):

    """ Stochastic file analysis- Case generation
    """
    #File analysis 
    Sto_List=Sto_Section(sto_file) # .sto file analysis

    #Fragements
    blo=Sto_List['BLOCKS']       #Block list 
    ind=Sto_List['INDEP']        #Independent list
    sce=Sto_List['SCENARIOS']    #Scenario list

    #Msg Error message 
    msg='Wrong stochastic specification\n'\
        +'.sto file must contain a SCENARIOS section\n'\
        +'or BLOCKS+INDEP sections'
    
    #-------------------
    #Case verification
    #-------------------

    #Case(1):Scenario case
    if len(sce)>0:

        #Verification (1): No indep nor block
        if len(blo)>0 or len(ind)>0:
            raise NameError(msg)
        else:
            case=Scenarios(sce,Root,Edge)
    #Case (2): Block + Indep Cases 
    else:

        #Verification (2): Empty indep and block
        if len(blo)==0 and len(ind)==0:
            raise NameError(msg)
        elif len(blo)==0:  #Only indep
            case=Indep(ind,Root)
            case.compute_tree(Edge)
        elif len(ind)==0: #Only blo
            case=Block(blo,Root)
            case.compute_tree(Edge)
        else:
            icase=Indep(ind,Root)
            bcase=Block(blo,Root)

            case=icase*bcase
            case.compute_tree(Edge)

    #--------------------
    #Return
    #--------------------
    return case
        
