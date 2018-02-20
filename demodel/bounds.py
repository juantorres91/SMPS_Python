from sets  import Set
from numpy import float64

__all__ = ['Bound']


def bounds_params(b_list, cont, inte):
    """
    Stores and classifies the bounds section

    Parameters
    ----------
    b_list : list
      bound string list
    cont : set
      continous variable set
    inte : set
      interger variable set
    """
    # UP= Upper bound, LO= Lower bound
    # FX= Fixed variable, UI= Upper integer    
    Bd = {'UP': {},'LO': {},'FX': {}, 'UI': {}}
    bkeys=Set(Bd.keys())

    # FR: Free variable, BV: Binary variable
    # MI: Non positive variable, PL: Non negative variable
    Ty = {'FR':Set(),'BV': Set(), 'MI': Set(), 'PL': Set()}
    tkeys = Set(Ty.keys())
    Tset = Set()  # Variable type verification

    # Output (3) bound delimiter
    delt = b_list[0][1]

    # Gathering information
    for u in b_list:

        # Verification (1): Number of line entries
        if len(u) < 3:
            raise NameError("Bound section more than 2 entires per line")

        # Verification (2): Vector name 
        elif  u[1]<>delt:
           raise NameError('Only one Bound vector is supported')

       # Verification (3) 
        elif u[2] not in cont and u[2] not in inte:
            raise NameError('Variable' + u[2] + 'is not defined' +
                            ' at the COLUMNS section .cor file\n' +
                            "Verify the BOUNDS Section")
        
        # Boubds analysis

        if u[0] in bkeys:

            #Verification (3): Line length
            if len(u)<>4:
                raise NameError('Bound parameters must have 4 entries per line:\n'\
                                +'(1) Bound type\n' \
                                +'(2) Bound vector name\n'\
                                +'(3) Variable name \n'\
                                +'(4) Bound value')

            #Verification (4): Repeated entry
            elif u[2] in Bd[u[0]]:
                raise NameError('Bound'+ u[0]+"," +u[2] \
                                +' cannot be defined twice\n' \
                                +'Verify BOUNDS -.cor file ')
            #Verification (5): Numeric entries
            try:
                #
                if (u[2] in inte) and (u[0] == 'UI'): 
                    Bd[u[0]][u[2]]=round(float(u[-1]))
                else:
                    Bd[u[0]][u[2]]=float(u[-1])
            except ValueError:
                print "Bound coefficient entry needs to be" \
                    +" numeric: \n" \
                    +"Verify .cor BOUNDS"+u[0]+","+u[2*j+1]
               
        #---------------------------------------------------------
        #Variable type case
        #----------------------------------------------------------
        elif u[0] in tkeys:

            #Verification (6): Line length
            if len(u)<>3:
                raise NameError('Variable type must have 4 entries per line:\n'\
                                +'(1) Variable type\n' \
                                +'(2) Bound vector name\n'\
                                +'(3) Variable name \n' )

            #Verification (7): Repeated value 
            elif u[2] in Tset:
                raise NameError('Variable type ' +u[2] \
                                +' cannot be defined twice\n' \
                                +'Verify BOUNDS -.cor file ')
            
            else:
                Ty[u[0]].add(u[2]) 
                Tset.add(u[2])
        #-----------------------------------------------------------
        #Not suported bound type
        #-----------------------------------------------------------
        else:
            #Not supported bound types
            raise NameError('Bound type '+u[0]\
                            +' is not supported')
    #Return 
    return Bd , Ty, delt

