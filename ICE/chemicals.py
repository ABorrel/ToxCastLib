from .chemical import chemical

class chemicals:
    """
    Entry point is the record to reduce the size of the structure
    """

    def __init__(self, l_lineICE):

        self.l_lineICE = l_lineICE

    def loadChem(self):

        self.d_chem = {}
        for lineICE in self.l_lineICE:
            casrn = lineICE["CASRN"]
            if not casrn in list(self.d_chem.keys()):
                self.d_chem[casrn] = chemical(lineICE)





