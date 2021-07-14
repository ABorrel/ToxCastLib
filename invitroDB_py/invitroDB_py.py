from Assays import Assays
from ICE import ICE



class invitroDB_py:

    def __init__(self, p_ICE, p_assays_summary):
        
        # path with the database
        self.p_ICE = p_ICE
        self.p_assays_summary = p_assays_summary
        
        # initialize classes
        self.c_Assays = Assays.Assays(self.p_assays_summary)
        self.c_ICE = ICE.ICE(self.p_ICE)
        
        self.err = 0

    def load_AssaysAndICE(self):
        self.c_Assays.loadAll()
        self.c_ICE.loadICE()




    def ratioActiveAssays(self, typeofCharac, cAssays):
    

        lcharac = cAssays.getlistCharac(typeofCharac)

        #print(lcharac)
        #print(cAssays.dassays.keys())

        dout = {}
        for charac in lcharac:
            dout[charac] = {"active":0, "inactive":0, "notest":0}

        if not "activeAssays" in self.__dict__:
            self.enrich = {}
            return

        for actAssays in self.activeAssays.keys():
            #print(cAssays.dassays[actAssays].charac[typeofCharac], "DDDD")
            charac = cAssays.dassays[actAssays].charac[typeofCharac]
            dout[charac]["active"] = dout[charac]["active"] + 1

        for inactAssays in self.inactiveAssays:
            charac = cAssays.dassays[inactAssays].charac[typeofCharac]
            dout[charac]["inactive"] = dout[charac]["inactive"] + 1

        for notest in self.notestAssays:
            charac = cAssays.dassays[notest].charac[typeofCharac]
            dout[charac]["notest"] = dout[charac]["notest"] + 1

        self.enrich = {}
        self.enrich[typeofCharac] = dout
