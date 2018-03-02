__all__=('dScen')

from ScenClass  import Scen
from copy       import copy
#--------------------------------------------------------
#Scen type (1): dScen() Independent distribution scenario
#Contains time structure
#--------------------------------------------------------
class dScen(Scen):

    """ 
    Constructor
    """
    def __init__(self):

        Scen.__init__(self) #Inheritance definition
          
        #Time structure
        self._ts=[]    #Ordered stage list
        self._pro={}   #St to st probability
        
        #Scenario coordinate
        self._cord={}  #Stage realizations

    #-----------------------------------
    #Properties
    #-----------------------------------
    @property
    def coordinate(self):
        return self._cord
    
    #------------------------------------
    #Methods
    #------------------------------------

    #Add new coordinate
    def add_coordinate(self, name,num, stage,pro=1):
        """
        Adds new realization coordinates
        """
        #Case (1) No stage structure 
        if len(self._ts)==0:
            pass
        #Case (2) Wrong stage name
        elif stage not in self._ts:
            raise NameError('Stage '+stage+' is not defined at the '\
                            +'.tim file')
        #Case (3) Update coordinate
        else:
            self._cord[stage][str(name)]=num #New coordinate
            self._pro[stage]*=pro

    #Set new stages
    def set_stages(self, ts):
        """ Defines scenario stages
        """
        #Time list 
        self._ts=ts

        for j in ts:
            self._cord[j]={}  #Initialize coordinate       
            self._pro [j]=1.0 #Initialize edge probability

    #Multiplication operation
    def __mul__(self,s1):

        """
        Combines two dScen objects
        """
        #Verification (1): Same time structure
        if self._ts<>s1._ts:
            raise NameError('Both scenarios must have the same'+\
                            ' ordered time periods')
        #New scenario
        s=dScen() #New scenario

        #----------------------------------------
        #Realizations  update
        #----------------------------------------
        for u in self._keys:
            #First scenario
            for i in self._rea[u]:
                s._rea[u][i]=self._rea[u][i]
            #Second scenario
            for j in s1._rea[u]:
                s._rea[u][j]=s1._rea[u][j]

        #---------------------------------------
        #Coordinates
        #---------------------------------------
        s.set_stages(self._ts) #Child time structure

        for u in self._ts :

            #First scenario
            for i in self._cord[u]:
                s._cord[u][i]=self._cord[u][i]
            #Second sceanrio
            for j in s1._cord[u]:
                s._cord[u][j]=s1._cord[u][j]
            #Stage probability
            s._pro[u]=self._pro[u]*s1._pro[u]
        
        #Return
        return s

    #-----------------------------------
    #Compute path
    def compute_path(self):

        #Verification (1): Time structure
        if len(self._ts)==0:
            raise NameError('dScenarios must have a list of'\
                            +' ordered time stages')
        else:
            
            #First stage: Root node
            cpath=['ROOT']            #Cumulative path

            #Inner stages
            for st in range(1, len(self._ts)-1):

                stage=self._ts[st]

                #Stage verification
                if len(self._cord[stage])>0:
                    c1=copy(cpath)     #Swallow copy
                    c1+=self._cord[stage].items()  #New elements

                    yield (cpath, c1),self._pro[stage], stage
                    cpath=c1           #Cumultative udate 
                    
            #Last stage
            stage=self._ts[-1]
            
            if len(self._cord[stage])>0:
                c1=copy(cpath)                 #Swallow copy
                c1+=self._cord[stage].items()  #New elements
                yield (cpath, c1),self._pro[stage], stage
                    
            else:
                c1=copy(cpath)      #Swallow copy
                c1+=stage           #New elements
                yield (cpath, c1), 1, stage
    
                    
                    
