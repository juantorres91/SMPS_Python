#Export
__all__=['Time_Section', 'Periods'] 


def Time_Section(timfile):
    """
    .tim file section classifier 
    """
    #Output dict
    Sections={'TIME':[], 'PERIODS':[], 'ROWS':[], 'COLUMNS':[]}
    keys=Sections.keys()

    #Ignored entries
    ign=['*','#']

    #.tim file
    fil=open(timfile,'r')
    sect=''                  #Current section

    #Gathering information 
    for x in fil:

        u=str.split(x)

        if u[0] in ign:              #Ignored entries case
            pass 
        elif 'ENDATA' in u[0]:       #File termination
            break
        elif u[0] in keys:           #Section change
            sect=u[0]
        else:

            #Validation (1)
            if sect=='':
                raise NameError('.tim file cannot be processed')
                break

            #Storing Sections
            Sections[sect].append(u)

    #Closing file
    return Sections

def Periods(p_list):
    """
    Period section analyser
    """

    #Output parameters
    Stages=list()        #Time Stages Ordered list
    Var=   dict()        #Variable to stage dict
    Rows=  dict()        #Rows ordered dict

    #Gathering information
    for u in p_list:

        #Validation (1):
        if len(u) <> 3:
            raise NameError ("PERIODS section must have 3 entries per line\n"
                             + "(1) Variable Name\n" \
                             + "(2) Row Name\n"\
                             + "(3) Stage Name \n")
            break
        #Store information
        Stages.append(u[-1])  #Stage list update
        Var[u[0]]=u[-1]       #Var update
        Rows[u[1]]=u[2]       #Rows update

    #Return
    return Stages, Var, Rows

#Testing


        
    
        
            
