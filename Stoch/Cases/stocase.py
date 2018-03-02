__all__=('StoCase')

from sets        import Set
from weakref     import ref
#-------------------------------
#Stochasticic case object
#-------------------------------
class StoCase(object):

    """
    Constructor
    """
    def __init__(self):

        self._names=Set()       #Scenario names
        self._ref={}            #Name to scenario reference
        self._list=[]           #Scenario list
        self._sc2node={}        #Scenario to node dict
        self._graph=None        #Sceario  directed graph

    #---------------------
    #Properties
    #---------------------
    @property
    def instances(self):
        return self._list

    @property
    def names(self):
        return list(self._names)

    @property
    def tree(self):
        return self._graph

    @property
    def reference(self):
        return self._ref

    @property
    def scenario_node(self):
        return self._sc2node
    
    #-----------------------
    #Methods
    #-----------------------

    #Add new scenario
    def add_scenario(self, s, distrib=True, name=''):
        """
        Inserts a scenario in the list 
        
        For probability driven lists it doesn't generates
        references 
        """

        #New scenario element
        self._list.append(s)

        #Explicit scenario case
        if distrib==False:
            self._names.add(name)
            self._ref[name]=ref(s)
        
    #Return scenario
    def scenario(self,name):
        """
        Returns scenario by reference
        """

        #Verification
        if name not in self._names:
            raise NameError('Scenario '+name+' not in sto case')
        else:
            return self._ref[name]()

    #Set node reference
    def set_node_reference(self, scen, node):
        """
        Stores scenario to parent node referece
        """
        self._sc2node[scen]=node
        
        
    #Set tree
    def set_stochastic_tree(self, tree):
        """
        Stores a new realization tree
        """
        self._graph=tree


    #Verification
    def verification(self,Root):
        """
        Verifies each scenario according the DeModel rules
        """
        for u in self._list:
            u.time_verification(Root)
    

        
