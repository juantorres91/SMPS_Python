from sets import Set
from numpy import float64

__all__ = ['row_param']


def row_param(r_list, Sotages=[], R_dic={}):
    """
    Categorizes rows per time and stage
    """

    # Validation (1): Time specifications
    if len(Stages) != len(R_dic):
        raise NameError("Number of rows in the .tim " +
                        "file must match the number of stages")
    # .cor output parameters
    rows = Set()                       # List of rows
    r_type = {'L': Set(), 'G': Set(),
              'E': Set(), 'N': []}     # List of constraints per type

    # .tim output parameters
    TS = {}         # Time-to row list container
    st = 0          # Stage counter
    ct = Stages[0]  # Current stage name
    TS = {}         # New dict elements

    for u in r_list:

        # Deterministic parameters

        # Verification (2): Number of line entries
        if len(u) != 2:
            raise NameError("ROWS section must have 2 entires" +
                            " per line")
        # Verification (3): Allowed equation types
        if u[0] not in r_type:
            raise NameError("Equation type " + u[0] +
                            " is not allowed for variable\n" + u[1])
        # Verification (4): Previously defined equation
        elif u[1] in rows:
            raise NameError("Equation: " + u[0] + " cannont be " +
                            "defined twice\n" +
                            "Verify ROWS -.cor file")
        else:
            rows.add(u[1])

            # Case: Objetive function evaluation
            if u[0] == 'N':
                r_type['N'].append(u[1])
            else:
                r_type[u[0]].add(u[1])  # Update equation type list

        # Time-wise parameters

        # Case (1): Objective function
        if u[0] == 'N':
            TS[u[1]] = Stages[-1]

            # Verification (5): Objective Function location
            if u[1] not in r_dic:
                pass
            elif st == 0:
                st += 1
            else:
                raise NameError("Objective function needs to be " +
                                " located at the first period")

        # Case(2):  Entry in .tim parameters
        elif u[1] in r_dic:

            # Verification (6): Rows must be ordered according .tim file

            if Stages[st] != r_dic[u[1]]:
                raise NameError(".cor ROW section does not follow " +
                                " the .tim Order")
            else:
                ct = Stages[st]  # Update current time
                st += 1          # Update time counter
                TS[u[1]] = ct    # Update time structure
        # Case (3):
        else:
            TS[u[1]] = ct

    return rows, r_type, TS
