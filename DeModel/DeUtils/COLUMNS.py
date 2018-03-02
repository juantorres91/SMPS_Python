#Export
__all__=('Columns')

#Import
from numpy       import   float64
from sets        import   Set

#------------------------------------------------------------
#Column Section Analyzer 
#------------------------------------------------------------
def Columns(col_l, row_l, Stages=[],V_dic={}, r2st={}):
    """ 
    Retrieves column information and clasiffies variables accoriding time
    col_l: Column List,    row_l: Constraint list
    Stages: Period orderd list,  V_dic:  Stage switch variable
    r2st:   Row to stage dict 
    """

    #Verification (1): Time specifications
    if len(Stages) <> len(V_dic):
        raise NameError("Number of columns in the .tim file must match the number of Stages")
    
    #.cor Output------------------------------------
    A=dict()         #Coefficient matrix dictionary
    I_Cond=False     #Integer Condition
    Cont=Set()       #Continuous variable list 
    Inte=Set()       #Integer Variable List
    Var=Set()        #Var set
    cv=''            #Current variable
    ci=False         #Current integer condition
    
    #.tim Output ------------------------------------
    TS={}             #Time to var dict
    st=0              #Current time period
    TimeKeys=Set()    #Time change keys
        
    ct=Stages[0]      #Name of the current time stage  
    
    #Gathering information
    for u in col_l:

        #-------------------------------------------------
        #Deterministic model parameters
        #-------------------------------------------------
        #Verification (2): Number of entries
        if len(u)%2<>1 or len(u)<3:
            raise NameError('Column '+u[0]+' constraint coeffients'\
                            +' are incomplete - .cor COLUMNS')
        #------------------
        # Integer condition
        #------------------
        if "'MARKER'" in u[1]:
        
            if "'INTEND'" in u[-1]:
                I_Cond=False
            elif "'INTORG'" in u[-1]:
                I_Cond=True

            #Verification (3): Incorrect condition 
            else:
                raise NameError(u[-1]+" is not a valid Integer"\
                                " variable delimiter\n "
                                " Verify COLUMNS - .cor file")
        else: 
            #Condition list update
            if I_Cond==True:
                Inte.add(u[0])
            else:
                Cont.add(u[0])

            #----------------------------------------------
            #Variable verification
            #----------------------------------------------
            
            #Verification (4): Previously defined variables
            if  u[0]<>cv and u[0] in Var:
                raise NameError("Variable "+u[0]+" cannot be"\
                                +' defined twice\n' \
                                +'Verify COLUMNS -.cor file ')

            #Verification (5): Variable type redefintion
            elif (u[0]==cv) and (ci<>I_Cond):
                raise NameError("Variable "+u[0]+ " cannot display "\
                                +"a double Integer & Continuous behaviour\n"\
                                +'Verify COLUMNS -.cor file') 
            else:
                cv=u[0]         #Update current variable
                Var.add(u[0])   #Update variable list
                ci=I_Cond       #Update integer condition
                
            #------------------------------------------------------
            #Time model parameters
            #------------------------------------------------------
            #Case (1):  Variables in the .tim file 
            if u[0] in V_dic:
                if u[0] in TimeKeys: #Repeated variable name
                    pass
                
                #Verification (6) : Vars  must be ordered according .tim file    
                elif Stages[st]<>V_dic[u[0]]:
                    raise NameError(".cor COLUMNS section does "\
                                    + "not follow the .tim Order")
                else:
                    ct=Stages[st]         #Update current time
                    st+=1                 #Update time counter
                    TS[u[0]]=ct           #Update time structure
                    TimeKeys.add(u[0])    #Update .tim var list
                        
            #Case (2): Variables outsie the .tim file
            else:
                TS[u[0]]=ct               #Update time structure

            #-----------------------------------------
            #Constraint linear coefficient analysis 
            #-----------------------------------------
            cons=(len(u)-1)/2  #Number of constraints per variable

            for j in range(0,cons):

                #Verification (7): Constraint in list
                if u[2*j+1] not in row_l:
                    raise NameError("Equation " +u[2*j+1] \
                                    + " is not defined at the "\
                                    + "ROW section .cor file\n"
                                    + "Verify COLUMNS -.cor file")

                #Verification (8): Repeated entries
                elif (u[2*j+1], u[0]) in A:
                    raise NameError ("Coefficient (" +u[0]+','+ u[2*j+1]\
                                     +') cannot be defined twice\n'\
                                     +'Verify COLUMNS -.cor file')

                #Verification (9): Numeric entries
                try: 
                    A[u[2*j+1], u[0]]=float(u[2*j+2]) #Update coefficient dict 
                except ValueError:
                    print "Column coefficient entry needs to be" \
                        +" numeric: \n" \
                        +"Verify .cor COLUMNS: "+u[0] +', '+u[2*j+1]

                #Verification (10): Variable-Constraint time missmatch                
                st_time=Stages.index(r2st[ u[2*j+1]])    #Constraint time
                if st_time<(st-1):
                    raise NameError('Variable-Constraint time mismatch')
                               
    #-----------------------
    #Return
    #-----------------------
    return A, Cont, Inte, TS
