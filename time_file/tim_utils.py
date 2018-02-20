__all__ = ['time_sorting', 'time_periods']
__version__ = '0.1'
__author__ = 'Juan J. Torres'


def time_sorting(timfile):
        
    """
    This function separates and organizes the .time file according
    the specific sections: TIME, PERIODS, ROWS and COLUMNS

    Parameters
    ----------
    timefile : str
      Name and path of .tim file

    Returns
    -------
    sect : dict
      Sorted elements of the .tim file
    """

    print "Reading time file" + timfile
    
    sect = {'TIME': [], 'PERIODS': [], 'ROWS': [], 'COLUMNS': []}
    se_cont = {'TIME': 0, 'PERIODS': 0,
               'ROWS': 0, 'COLUMNS': 0}  # Entry counter
    ign = ['*', '#']  # Ignored entries

    fil = open(timfile, 'r')  # Opening file
    c_s = ''  # Current section

    for x in fil:
        u = str.split(x)

        if u[0] in ign:         # Ignored entries case
            pass 
        elif 'ENDATA' in u[0]:  # File termination
            break
        elif u[0] in sect.keys():   # Section change
            c_s = u[0]
            se_cont[c_s] += 1

            if se_cont[c_s] > 1:  # Validation 2
                raise NameError('Section' + c_s
                                + ' should be defined once')
        else:
            if c_s == '':  # Validation (1)
                raise NameError('.tim file cannot be processed')
                break

            sect[c_s].append(u)  # Stores section elements

    fil.close()            
    return sect


def time_periods(p_l):
        
    """
    This function analyses the PERIOD section

    Parameters
    ----------
    p_l : list
      PERIOD section content
    
    Returns
    -------
    stages : list
      list of time stages
    var : dict
      variable to stage header
    rows : dict
      constraint to stage header
    """
    
    stages = list()    # Time stages
    var = dict()       # Variable to stage dict
    rows = dict()      # Rows ordered dict

    for u in p_l:

        # Validation (1):
        if len(u) != 3:
            raise NameError("PERIODS section must have 3 entries per line\n"
                            + "(1) Variable Name\n"
                            + "(2) Row Name\n"
                            + "(3) Stage Name \n")
            break
        
        stages.append(u[-1])  # Stage list update
        var[u[0]] = u[-1]     # Var update
        rows[u[1]] = u[2]     # Rows update

    print str(len(stages)) + ' Stages'
    return stages, var, rows

