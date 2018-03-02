from sets import Set

def Sto_Section(stofile):
    """
    .sto file section classifier
    """

    #Output dict
    Sections={'STOCH':[], 'SIMPLE':[], 'SCENARIOS':[], \
              'INDEP':[],'BLOCKS':[]}
    keys=Set(Sections.keys()) #Section names

    #Ignored entries
    ign=tuple(['*','#'])
    bre=False           # ENDATA existance
    
    #.tim file
    fil=open(stofile,'r')
    sect=''                  #Current section

    #Gathering information 
    for x in fil:

        u=str.split(x) #Stores line separated by spaces
    
        if len(u)==0:              #Empty line
            pass 
        elif u[0].startswith(ign): #Ignored entries case
            pass 
        elif 'ENDATA' in u[0]:     #File termination
            bre=True                 
            break
        elif u[0] in keys:         #Section change
            sect=u[0]

        #Validation (1):Non suported sections 
        elif len(u)==1:
            raise NameError('Stochastic section '+ u[0]+ \
                            ' is not supportted')
        else: 
            #Validation (2): Non valid previous section
            if sect=='':
                raise NameError('.sto file cannot be processed')

            #Storing Sections
            Sections[sect].append(u)

    #Verification(3): ENDATA existance
    if bre==False:
        raise NameError('.sto file must have a ENDATA line') 
            
    #Closing file
    return Sections

if __name__=="__main__":
    import sys

    S=Sto_Section(sys.argv[1])
    print S
