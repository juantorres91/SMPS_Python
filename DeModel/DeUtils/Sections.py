from sets import Set

def Cor_Section(corfile):
    """
    .cor file section classifier 
    """
    #Output dict
    Sections={'NAME':[], 'ROWS':[], 'COLUMNS':[], \
              'RHS':[],'RANGES':[], 'BOUNDS':[]}
    keys=Set(Sections.keys()) #Section names

    #Ignored entries
    ign=tuple(['*','#'])
    bre=False                       # ENDATA existance
    
    #Vector- names
    vector=['RHS','BOUNDS', 'RANGES'] # Sections with vector names 

    #.tim file
    fil=open(corfile,'r')
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
            if u[0] in vector and len(u)>2: 
                Sections[sect].append(u)    #RHS, RANGE a vector names
            else:
                sect=u[0] #Section update
        elif len(u)==1:                  

            #Verification (1): Invalid keys
            raise NameError('Section '+u[0]\
                            +'cannot be processed')
        else:
            #Verification(2):Invalid data entry-unprecedented section
            if sect=='':
                raise NameError('.cor file cannot be processed')

            #Storing Sections
            Sections[sect].append(u)

    #Verification(4): ENDATA existance
    if bre==False:
        raise NameError('.cor file must have a ENDATA line') 
            
    #Closing file
    return Sections

if __name__=="__main__":
    import sys

    S=Cor_Section(sys.argv[1])
    print S['RHS']
