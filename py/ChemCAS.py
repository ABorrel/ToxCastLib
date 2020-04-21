def fromatLineChem(lineChem):

    # format split \n
    llineChem = list(lineChem)
    i = 0
    imax = len(llineChem)
    flagopen = 0
    while i < imax:
        if llineChem[i] == "\"" and flagopen == 0:
            flagopen = 1
        elif llineChem[i] == "\"" and flagopen == 1:
            flagopen = 0

        if flagopen == 1 and llineChem[i] == "\n":
            llineChem[i] = " "
        elif flagopen == 1 and llineChem[i] == ",":
            llineChem[i] = " "

        i = i + 1

    lineChem = "".join(llineChem)
    lineChem = lineChem.replace("\"", "")

    return lineChem



class ChemCAS:

    def __init__(self, lineChem):

        self.lineChem = fromatLineChem(lineChem)


    def setChem(self):

        lsplit = self.lineChem.strip().split(",")

        self.chid = lsplit[0]
        self.name = lsplit[1]
        self.CASID = lsplit[2]
        code = lsplit[3]
        self.code = code
        self.dsstoxID = lsplit[4]
        self.origin = lsplit[5]



    def setIC50(self, lassaysin, lassaysAll, lIC50, verbose = 0):

        """
        param:
        - lassaysin: preselected list of assays
        - assayAll: all assays 
        """

        i = 1
        imax = len(lIC50)
        lnotest = []
        dactive = {}
        linactive = []

        if verbose == 1: print(lIC50)

        if lassaysin == []: # case no specific assays
            while i < imax:
                AC50 = lIC50[i]
                if AC50 == "NA":
                    lnotest.append(lassaysAll[i])
                elif AC50 == "1e+06":
                    linactive.append(lassaysAll[i])
                else:
                    dactive[lassaysAll[i]] = AC50
                i += 1
        else:
            while i < imax:
                AC50 = lIC50[i]
                assay = lassaysAll[i]
                if not assay in lassaysin:
                    i = i + 1
                    continue
                if AC50 == "NA":
                    lnotest.append(lassaysAll[i])
                elif AC50 == "1e+06":
                    linactive.append(lassaysAll[i])
                else:
                    dactive[lassaysAll[i]] = AC50
                i += 1

        self.activeAssays = dactive
        self.notestAssays = lnotest
        self.inactiveAssays = linactive



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
