#Export
__all__=('SBound')

#-----------------------------------------
#Scenario bounds- Conectivity verification
#-----------------------------------------
class SBound(object):
    """
    Constructor
    """
    def __init__(self):
        self._lo=0            #Scenario definition time
        self._up=float('inf') #Scenario lower time sepatation time 

        #Error message
        self._msg='Scenario tree is not properly defined' 

    #-------------------------------    
    #Properties---------------------
    #-------------------------------
    @property
    def min(self):
        return self._lo

    @property
    def max(self):
        return self._up 

    #-------------------------------
    #Methods------------------------
    #-------------------------------
    #Set definition time 
    def set_min(self, lo):

        #Verification(1): Branching before definition time
        if lo> self._up:
            raise NameError(self._msg)
        else:
            self._lo=lo

    #Set lower separation time
    def set_max(self, up):

        #Verification (1): branching before the definition time
        if up<self._lo:
            raise NameError(self._msg)
        elif up<self._up:
            self._up=up         
