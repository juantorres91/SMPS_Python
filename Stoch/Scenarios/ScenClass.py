__all__=('Scen')

from sets import Set
#-----------------------------------
#Scenario object 
# ----------------------------------
class Scen():

    """
    Constructor
    """
    def __init__(self):

        #Model possible realizations
        self._rea={'BL':{},'RHS':{},'RANGES':{},\
                   'UP':{},'LO':{},'UI':{},'FX':{}} 
        self._keys=self._rea.keys()        #Realization names 
        
        #Delimiters set
        self._delt={'RHS':'','RANGES':'','BOUNDS':''}

        #Bound names
        self._bd=Set(['UP','LO','FX','UI'])

        #Time (Block - Indep Only)
        self._time=''   #Verification time

        #Constraint set
        self._cons=Set()

        #Variable set
        self._var=Set()
        
    #------------------------------------------------------------
    #Properties
    #------------------------------------------------------------
    @property
    def realizations(self):
        return self._rea

    #-------------------------------------------------------------
    #Methods
    #-------------------------------------------------------------

    #Add new realizations
    def add_realization(self, val,names):
        """Insert rhs realization
        """

        #Verification (1): Numeric values
        try:
            rea=float(val)
        except:
            raise NameError('Realizations must be numeric')

        #Verification (2): Number of names:
        if len(names)==2:

            self._cons.add(names[1])  #Constraint set update
            
            #Case (1): RHS
            if names[0]==self._delt['RHS']:
                self._rea['RHS'][names[1]]=rea    
            #Case (2): RANGES 
            elif names[0]==self._delt['RANGES']:
                self._rea['RANGES'][names[1]]= rea
            #Case (3): Block coefficient
            else:
                self._rea['BL'][(names[1], names[0])]=rea
                self._var.add(names[0]) #Variable set update
                
        #Case (4): Bounds
        elif len(names)==3:

            #Verification (3): delt == bound/allowed bound names
            if (names[0] in self._bd) and (names[1]==self._delt['BOUNDS']):
                self._rea[names[0]][names[2]]= rea
                self._var.add(names[2]) #Variable set update
                
            elif names[1]<>self._delt['BOUNDS']:
                raise NameError('Bound vector '+ names[1]+\
                                " was not specified at the .cor file")
            else:
                raise NameError('Bound type '+names[0]+\
                                " is not supported")
            #Wrong number of names
        else:
            raise NameError('Realization '+ names+' cannot be processed')

    #----------------------------------
    #Set bound, range, rhs vector names
    #----------------------------------
    def set_delimiters(self, rhs='', ran='', bound=''):
        """ Sets scenario delimiter 
        """
        self._delt={'RHS':rhs,'RANGES':ran, 'BOUNDS':bound}

    #----------------------------------
    #Time verification
    #---------------------------------
    def time_verification(self, Root):
        """
        Time realization verification
        Root:   Deterministic model
        """
        #Verification (1) Up- Ui intersection
        up= self._rea['UP'].keys()
        ui= self._rea['UI'].keys()   
        inter= set(up).intersection(ui) 

        if len(inter)>=1:
            raise NameError('UP bound parameters cannot be '\
                            +'redefined as UI .sto file')

        #Verification (2) Range type equations
        ran=Root.ranges_constraints()
        ran2=Set(self._rea['RANGES'].keys())
        
        if not ran2.issubset(ran):
            raise NameError('Ranges can only be defined at'\
                            +' the .cor file')

        #--------------------------------------
        #Case (1): Constraint time verification
        #-------------------------------------
        for u in self._cons:

            #Verification (3): Constraint in list
            try:
                time=Root.st_to_cons[u]

                #Verification (4): Realization time
                if  '' <> self._time <> time:
                    raise NameError('Constraints at the .sto '\
                                    +'file do not match the '\
                                    +'.tim file')  
            except:

                raise NameError('Constraints at the .sto file'\
                                +' do not match the .cor file')
        #--------------------------------------
        #Case (2): Variable time verification
        #--------------------------------------
        for u in self._var:

            #Verifiation (5): Variable in list 
            try:
                time=Root.st_to_var[u]

                #Verification (6): Realization time
                if  '' <> self._time <> time:
                    raise NameError('Variables at the .sto '\
                                    +'file do not match the '\
                                    +'.tim file')
            except:
                raise NameError('Variables at the .sto file'\
                                +' do not match the .cor file')
        #--------------------------------------
        #Case (3): Constraint-Variable time verification 
        #--------------------------------------

        #Verification time 
        if self._time=='':
            st=0
        else:
            st=Root.stages.index(self._time)
            
        #Constraint keys verification 
        for u in self._rea['BL']:

            #Verification (7): Var-Time in list
            try:
                c_stage=Root.st_to_cons[u[0]] #Constaint stage
                v_stage=Root.st_to_var [u[1]] #Variable stage
        
                c_time=Root.stages.index(c_stage) #constraint time  
                v_time=Root.stages.index(v_stage) #Variable time

                #Verification (8): Realization time
                if v_time>c_time:
                    raise NameError('Variable-Constraint time mismatch\n'\
                                    +'Verify the .sto file')
                elif st>0:
                    if c_time<>st:
                        raise NameError('Wrong realization time for coefficent:\n'\
                                        +str(u[0])+' '+str(u[1])+' .sto file')
                        
            except:
                raise NameError('Block coefficients at the .sto file'\
                                +' do not match the .cor file')          
            

    #-----------------------------------
    #Set realization time
    #-----------------------------------
    def set_time(self, time):
        """
        Sets realization time
        """
        self._time=time 
        
    #-----------------------------------
    #Derived scenario parameters
    #-----------------------------------
    def der_realization(self, s1):
        """ 
        Set derived scenario parameters
        s1: Parent scenario
        """
        
        #Realization loop
        for i in s1._keys:

            for j in s1._rea[i]:

                #Realization verification
                if j not in self._rea[i]:
                    self._rea[i][j]=s1._rea[i][j]
            
            
            
    
