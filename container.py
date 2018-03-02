#Export
__all__=('VarContainer')

#Import
from sets import Set

#--------------------------------------
#Variable average/ min-max container
#--------------------------------------
class VarContainer(object):
    """
    Constructor
    """

    def __init__(self,pro=1):
        
        self._cont={}     #Continuous variables
        self._pro= pro    #Scenario probability

    #-----------------------------
    #Properties
    #-----------------------------

    @property
    def probability(self):
        return self._pro

    @property
    def sol(self):
        return self._cont

    #--------------------------------
    #Methods
    #--------------------------------
    def add_var(self,key,val):
        self._cont[key]=val
