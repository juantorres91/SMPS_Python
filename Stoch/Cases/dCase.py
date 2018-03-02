__all__=('dStoCase', 'Cartesian')

from stocase     import StoCase
from weakref     import ref
from networkx    import (DiGraph,get_node_attributes)

#----------------------------------
#Discrete distribution stochastic case obect
#---------------------------------
class dStoCase(StoCase):

    """
    Constructor
    """
    def __init__(self,ts):

        StoCase.__init__(self) #Inheritance definition

        #Model atributes
        self._ts=ts            #Ordered period list 
                    
    #----------------------------
    #Methods
    #----------------------------
        
    #Combines two scenario lists
    def __mul__(self,s1):

        """
        Scenario case combination - permutation
        """
        s=dStoCase(self._ts) #New stocase

        # Loop
        for u in self._list:
            for v in s1._list:
                s.add_scenario(u*v)

        #return
        return s

    #Compute realization tree
    def compute_tree(self, Edge=False):

        #Case realization tree
        G=DiGraph()                  #Ordered graph
        G.add_node('ROOT', stage=self._ts[0],
                   probability=1.0)  #Root node

        #Auxiliar variables 
        node={}                     #Node container
        count={}                    #Realization counter
        node[0]={('ROOT',): 'ROOT'} #Root instance
        sc_num=0                    #Number of scenarios
        
        for i in range(1,len(self._ts)) :
            node [i]={}
            count[i]=0 

        #----------------------
        #Scenario path analysis
        #----------------------
        for u in self.instances:

            de=1        #Graph depht counter
            sc_num+=1   #Number of scenarios update
            
            #Node - edge construction
            for gen in u.compute_path():

                #-----------------------------
                #Node construction
                #-----------------------------
                n1_tp=tuple(gen[0][1]) #N1 tuple representation
                n0_tp=tuple(gen[0][0]) #N0 tuple representation
                pr=gen[-2]             #Arc conditional probability
                
                #Case (1): Entering node verification
                try:
                    n_in=node[de][n1_tp] 

                #Case (2): New node
                except:
                    count[de]+=1
                    n_in='Node_'+str(de)+'_'+str(count[de])

                    #Tree update
                    node[de][n1_tp]=n_in

                    #Probability reference
                    # True-Probability at edge
                    # False- Probability at node
                    if Edge: 
                        G.add_node(n_in, stage=gen[-1])    
                    else:
                        G.add_node(n_in, stage=gen[-1],
                                   probability=float(pr))        
                #----------------------------
                #Edge construction
                #----------------------------
                n_out=node[de-1][n0_tp]
                G.add_edge(n_out, n_in)   #Node atribute

                #Probability reference
                if Edge:
                    G.edge[n_out][n_in]['probability']=float(pr)
                
                #----------------------------
                de+=1      #Depth update
 
            #-----------------------------------
            #Reference construction
            #-----------------------------------
            nam='Scenario'+str(sc_num)    #Scenario name
            G.node[n_in]['scenario']=nam #Scenario to node
            self._names.add(nam)          #Object name update 
            self._ref[nam]=ref(u)         #Scenario reference
            self._sc2node[nam]=n_in       #Node2scenario reference
            
            
        #Del
        del node
        del count
                
        #Graph assigment
        self._graph=G 
        

#--------------------------------------------
#Permutation
#--------------------------------------------
def Cartesian(List):
    """
    Returns the permutation of a list of sctochastic cases
    """
    s=List[0]

    for j in range(1, len(List)):
        s*=List[j] 

    return s
