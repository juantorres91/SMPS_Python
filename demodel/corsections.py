from sets import Set

__all__ = ['cor_section']


def cor_section(corfile):
    """
    This function separates and organizes the .cor file according
    the specific sections: NAME, ROWS, COLUMNS, RHS, RANGES and
    BOUNDS

    Parameters
    ----------
    corfile : str
      Name and path of .cor file

    Returns
    -------
    sect : dict
      Sorted elements of the .cor file
    """

    sect = {'NAME': [], 'ROWS': [], 'COLUMNS': [],
            'RHS': [], 'RANGES': [], 'BOUNDS': []}

    ign = tuple(['*', '#'])  # Ignored entries
    bre = False       # ENDATA existance

    vector = ['RHS', 'BOUNDS', 'RANGES']  # Sections with vector names

    # cor analysis
    fil = open(corfile, 'r')
    c_s = ''  # Current section

    for x in fil:

        u = str.split(x)

        if len(u) == 0:              # Empty line
            pass
        elif u[0].startswith(ign):   # Ignored entries case
            pass
        elif 'ENDATA' in u[0]:       # File termination
            bre = True
            break
        elif u[0] in sect:           # Section change
            if u[0] in vector and len(u) > 2:
                sect[c_s].append(u)  # RHS, RANGE a vector names
            else:
                c_s = u[0]           # Section update
        elif len(u) == 1:
            # Verification (1): Invalid keys
            raise NameError('Section ' + u[0] +
                            'cannot be processed')
        else:
            # Verification(2):Invalid data entry-unprecedented section
            if sect == '':
                raise NameError('.cor file cannot be processed')
            sect[c_s].append(u)

    # Verification(4): ENDATA existance
    if bre is False:
        raise NameError('.cor file must have a ENDATA line')

    return sect
