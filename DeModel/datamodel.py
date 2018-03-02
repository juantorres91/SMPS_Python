from sets       import Set
from DeUtils    import *
from SMPS.Time  import (Time_Section,Periods)

#------------------------------------------
#(MI)LP deterministic models
#------------------------------------------
__all__=("DataModel")

class DataModel(object):

    """
    Constructor
    """
    def __init__(self, corfile, timfile):

        #----------------------------
        #File analysis
        #----------------------------
        CFile=Cor_Section(corfile)   #.cor parameters
        TFile=Time_Section(timfile)  #.tim parameters

        #Time analysis
        Stages, var_d, rows_d=Periods(TFile['PERIODS'])
        del TFile

        #Core analysis
        ROWS=CFile['ROWS']       #Rows list
        COLUMNS=CFile['COLUMNS'] #Column list
        RHS=CFile['RHS']         #RHS  list
        RANGES=CFile['RANGES']   #Ranges constraints
        BOUNDS=CFile['BOUNDS']   #Bounds list
        del CFile
        
        #-----------------------------
        #Row section
        #-----------------------------
        #Verification (1):
        if len(ROWS)== 0:
            raise NameError('Rows section cannot be empty')

        #Row data assignment
        rows, r_type, r_ts=Rows(ROWS,Stages, rows_d)
        del ROWS

        #-----------------------------
        #Column section
        #-----------------------------
        #Verification (2)
        if len(COLUMNS)==0:
            raise NameError('Column section cannot be empty')
        
        #Column data assignment
        mat, cont, inte, v_ts=Columns(COLUMNS,rows, Stages, var_d, r_ts)
        del COLUMNS

        #----------------------------
        #RHS section 
        #----------------------------
        #Verification (3)
        if len(RHS)==0:
            raise NameError('RHS section cannot be empty')
        rhs, rh_del=Rhs(RHS, rows)

        #--------------------
        #Model Attributes
        #--------------------

        #Time structures---
        self._Stages=Stages    #Problem stages
        self._r_ts=r_ts        #Stage constraints
        self._v_ts=v_ts        #Stage variables

        #Constraints 
        self._const=rows       #Constraint set
        self._conty=r_type     #Constraint type
        self._coef=mat         #Coefficient matrix        
        
        #Variables---------
        self._iv=inte          #Integer variables 
        self._cv=cont          #Non integer variables

        #Bounds-------------
        if  len(BOUNDS)>0:

            Bd, Ty, bd_del=Bounds(BOUNDS,cont, inte)
            self._bound= Bd       #Variable bounds
            self._type=  Ty       #Variable type
            self._bdelt= bd_del   #Bound delimiter

        else:
            self._bound= None  #Variable bounds
            self._type=  None  #Variable type
            self._bdelt= ''    #Bound delimiter
            
        #Rhs/range---------
        self._rhs=rhs          #Right hand side
        self._rhdel=rh_del     #RHS delimiter

        if  len(RANGES)>0:     

            ran, randel=Rhs(RHS, rows)
            self._ranges=ran       #Range coefficients
            self._ran_del=randel   #Ranges vector name
        else:
            self._ran_del=''
    
        
    #--------------------
    #Properties
    #--------------------

    #Time-----------
    @property
    #Stage ordered list
    def stages(self):
        return self._Stages

    @property
    #Stage to variable
    def st_to_var(self):
        """ Stage to variable"""
        return self._v_ts
    
    @property
    #Stage to constraint
    def st_to_cons(self):
        """Stage to constraint"""
        return self._r_ts

    #Constraints---------
    @property
    #Constraint list
    def constraints(self):
        return self._const 

    @property
    #Constraint type
    def constraint_type(self):
        return self._conty

    @property
    #Coefficient matix
    def matrix(self):
        return self._coef             
    
    #Variables----------
    @property 
    #Model variables
    def variables(self):
        return self._iv | self._cv

    @property
    #Integer variables
    def integer_variables(self):
        return self._iv
    
    #rhs---------------------------
    @property
    #RHS vector 
    def rhs(self):
        return self._rhs

    #--------------------------------------------
    #Methods (1): Ret
    #--------------------------------------------
    def free_variables(self):
        """ Returns model free variables 
        """ 
        try:
            return self._bd['FR']
        except:
            return Set()

    def negative_variables(self):
        """ Returns model negative variables
        """
        try:
            return self._bd['MI']
        except:
            return Set()

    def upbound(self):
        """ Returns the colection of up bounds
        """
        try:
            return self._bound['UP']   #Variable bounds
        except:
            return Set()

    def lobound(self):
        """ Returns the colections of lower bounds
        """
        try:
            return self._bound['LO']
        except:
            return Set()

    def uibound(self):
        """ Returns upper integer bounds
        """
        try:
            return self._bound['UI']
        except:
            return Set()

    def binary_variables(self):
        """" Returns the binary variables set"""
        try:
            return self._bd['BV']
        except:
            return Set()

    def fixed_variables(self):
        """ Returns fixed variables
        """
        try:
            return self._bound['FX']
        except:
            return Set()
            
    def ranges_constraints(self):
        """ Returns range type constraints
        """
        try:
            return Set(self._ranges.keys())
        except:
            return Set()

    def ranges_coefficients(self):
        """Returns range coefficients
        """
        try:
            return self._ranges
        except:
            return {}

    def delimiters(self):
        """ Returns RHS/BOUND/Vector names
        """
        return {'RHS': self._rhdel, 'RANGES':self._ran_del,\
                'BOUNDS': self._bdelt}
    
#Testing
if __name__=='__main__':
    import sys

    x=DataModel(sys.argv[1], sys.argv[2]) 
 
