#export
__all__=['Rhs']

#Import
from numpy       import   float64
from sets        import   Set

#------------------------------------------------------------
#RHS/Range Section Analyzer 
#------------------------------------------------------------
def Rhs(r_lis, row_l, name='RHS'):
    """
    Stores Rhs/Range Parameters
    """
    #Output parameters:
    rhs={}            #RHS/range dict
    delt=r_lis[0][0] #RHS vector name  
    
    #Gathering information
    for u in r_lis:

        #Verification (1): Number of entries  
        if len(u)%2<>1 or len(u)<3:
            raise NameError('Rhs '+u[0]+' coeffients'\
                            +' are incomplete - .cor'+name)

        #Verification (2): Rhs Vector Name
        elif u[0]<>delt:
           raise NameError('Only one'+ name+' vector is supported')
        
        else:      
            #Line iteration 
            cons=(len(u)-1)/2  #Number of rhs per line

            for j in range(0,cons):

                #Verification (3): Repeated entry
                if u[2*j+1] in rhs:
                    raise NameError('Rhs'+ u[1]+ "cannot be"\
                                    +' defined twice\n' \
                                    +'Verify '+name +' -.cor file ')

                #Verification (4): rhs in constraint list
                elif u[2*j+1] not in row_l:
                    raise NameError("Equation " +u[2*j+1] \
                                    +" is not defined at the "\
                                    +"ROW section .cor file\n"
                                    +"Verify the "+name+"  Section")

                #Verification (5): Numeric enties
                try:
                    rhs[u[2*j+1]]=float(u[2*j+2])
                except ValueError:
                    print "RHS coefficient entry needs to be" \
                        +" numeric: \n" \
                        +"Verify .cor " +name + " "+u[2*j+1]      

    #--------------------
    #Return
    #-------------------
    return rhs, delt
