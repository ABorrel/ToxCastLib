from copy import deepcopy

from .chemical import chemical
from .record import record

class ICE:

    def __init__(self, p_ICE):

        self.p_ICE = p_ICE


    def load_ICE(self):

        l_linesICE = loadMatrixToList(self.p_ICE)
        self.load_AllRecord(l_linesICE)


    def load_AllRecord(self, l_linesICE):

        self.resultEndpoint = {}
        self.chemicals = {}

        i = 1
        imax= len(l_linesICE)
        for lineICE in l_linesICE[1:]:
            l_elem = lineICE.split("\t")
            if i % 100000 == 0:
                print("Load %s/%s"%(i, imax))
            i = i + 1
            
            casrn = l_elem[3]
            try: self.chemicals[casrn]
            except: self.chemicals[casrn] = chemical(l_elem)

            endpoint = l_elem[5]
            try: self.resultEndpoint[endpoint]
            except: self.resultEndpoint[endpoint] = record()
                
            
            self.resultEndpoint[endpoint].CASRN.append(l_elem[3])
            self.resultEndpoint[endpoint].RecordID.append(l_elem[1])
            self.resultEndpoint[endpoint].Curve.append(l_elem[6])
            self.resultEndpoint[endpoint].QC.append(l_elem[7])
            self.resultEndpoint[endpoint].TestRange.append(l_elem[8])
            self.resultEndpoint[endpoint].TestRangeUnit.append(l_elem[9])
            self.resultEndpoint[endpoint].Endpoint.append(l_elem[10])
            self.resultEndpoint[endpoint].Response.append(l_elem[11])
            self.resultEndpoint[endpoint].ResponseUnit.append(l_elem[12])



    def get_resultsByEndpoints(self, aenm):
        if not "resultEndpoint" in self.__dict__:
            self.load_ICE()

        return deepcopy(self.resultEndpoint[aenm])



