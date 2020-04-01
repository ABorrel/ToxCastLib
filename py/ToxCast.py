from copy import deepcopy
from os import path
import numpy
from re import search

import Assays
import ChemCAS
import runForToxCast
import toolboxToxCast

# define the dataset folder
PR_DATA = "/home/borrela2/data/"




class ToxCast:

    def __init__(self, lsources, prresults, pchem = "", pAC50 = "", passays=''):

        if pchem == "" or pAC50 == "" or passays == "":
            self.pchem = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/Chemical_Summary_190226.csv"
            self.pAC50 = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/ac50_Matrix_190226.csv"
            self.passays = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/Assay_Summary_190226.csv"
        else:
            self.pchem = pchem
            self.pAC50 = pAC50
            self.passays = passays

        self.lsource = lsources
        self.prresults = prresults
        self.version = "InVitroDB 3.1"
        self.update = "March-2019"


    def loadAssays(self, lassays=[]):

        fassays = open(self.passays, "r", encoding="utf8", errors='ignore')
        blockassays = fassays.read()
        fassays.close()

        llassays = toolboxToxCast.fromatAssaysBlock(blockassays)
        dout = {}
        for lassay in llassays:
            cassays = Assays.Assay(lassay)
            nameAssay = cassays.charac["assay_component_endpoint_name"]
            if lassays != [] and not nameAssay in lassays:
                continue

            if self.lsource != []:
                #print cassys.charac["assay_source_name"]
                if cassays.charac["assay_source_name"] in self.lsource:
                    dout[nameAssay] = cassays
            else:
                dout[nameAssay] = cassays

        self.dassays = dout

    def getUniqueAssayCharac(self, typeCharac):
        if not "dassays" in self.__dict__:
            self.loadAssays()

        lout = []
        for assay in self.dassays.keys():
            try: lout.append(self.dassays[assay].charac[typeCharac])
            except: pass
        
        lout = list(set(lout))
        return lout

    def getAssaysByCharacVal(self, characK, characV):
        if not "dassays" in self.__dict__:
            self.loadAssays()

        lout = []
        for assay in self.dassays.keys():
            if characK in list(self.dassays[assay].charac.keys()):
                if self.dassays[assay].charac[characK] == characV:
                    lout.append(assay)
        return lout
    

    def getChemTestedByAssays(self, assay_name):
        if not "dassays" in self.__dict__:
            self.loadAssays()

        if not "dchem" in self.__dict__:
            self.loadChem()
            self.loadAC50()
        
        dchemTested = self.loadAC50forAssay(assay_name, notest=0)
        return list(dchemTested.keys())


    def writeAssaysTable(self, lprop, prout):

        if not "dassays" in self.__dict__:
            self.loadAssays()
        
        pfilout = prout + "AssaysTable.csv"
        filout = open(pfilout, "w")
        filout.write("name\t%s\n"%("\t".join(lprop)))
        for assay in self.dassays.keys():
            filout.write("%s\t%s\n"%(assay, "\t".join([str(self.dassays[assay].charac[prop]) for prop in lprop])))
        filout.close()
        return pfilout


    def removeNoTargetedAssays(self):
        """
        Dell assays without interest for chemical prediction i.e. interference assays / channel (keep only ratio) 
        """
        i = 0
        lassays = list(self.dassays.keys())
        imax = len(lassays)
        while i < imax:
            nameAssays = lassays[i]
            if search("TOX21_AutoFluor", nameAssays):
                del self.dassays[lassays[i]]
                del lassays[i]
                imax = imax - 1
            elif nameAssays.split("_")[-1] == "ch1" or nameAssays.split("_")[-1] == "ch2":
                del self.dassays[lassays[i]]
                del lassays[i]
                imax = imax - 1
            else:
                i = i + 1


    def loadAC50byassays(self):
        """
        Not used because slow
        """
        if not "dassays" in self.__dict__:
            self.loadAssays()

        if not "dchem" in self.__dict__:
            self.loadChem()
            self.loadAC50()

        print("Load")
        dout = {}

        fAC50 = open(self.pAC50, "r")
        lchemAC50 = fAC50.readlines()
        fAC50.close()

        lassays = lchemAC50[0].strip().split(",")
        nbassays = len(lassays)

        ichem = 1
        for assayAC50 in lchemAC50[1:500]:
            lChemAC50 = assayAC50.strip().split(",")
            chemID = lChemAC50[0]
            chemID = chemID.replace("\"", "")
            CASID = self.convertIDtoCAS(chemID)
            ichem = ichem + 1
            if ichem%100 == 0:
                print("Load: ", ichem)

            if CASID != "ERROR":
                i = 0
                while i < nbassays:
                    assay = lassays[i]
                    if not assay in list(dout.keys()):
                        dout[assay] = {}
                    dout[assay][CASID] = lchemAC50[i + 1]
                    i = i + 1

        self.dassaysAC50 = dout


    def getTopActive(self, assay, ntop):

        dAC50 = self.loadAC50forAssay(assay, notest=0)
        lchem = list(dAC50.keys())
        lval = list(dAC50.values())
        vval = numpy.array(lval)
        litop = numpy.argsort(vval)
        return [lchem[i] for i in litop[:ntop]]


    def loadChem(self, ):

        self.dchem = {}

        fchem = open(self.pchem, "r", encoding="utf8", errors='ignore')
        llineChem = fchem.readlines()
        fchem.close()

        for lineChem in llineChem[1:]:
            # format to split on comma
            cchem = ChemCAS.ChemCAS(lineChem)
            cchem.setChem()

            self.dchem[cchem.CASID] = cchem


    def loadChemSpFilter(self, cutoffActive):

        pchemfilout = self.prresults + "chem_" + str(cutoffActive)
        passaysfilout = self.prresults + "assays_" + str(cutoffActive)

        #if path.exists(pchemfilout) and path.exists(passaysfilout):
        #    self.filterToxCast = toolbox.loadMatrixToList(pchemfilout)
        #    return [pchemfilout, passaysfilout]

        if not "dassays" in self.__dict__:
            self.loadAssays()

        if not "dchem" in self.__dict__:
            self.loadChem()
            self.loadAC50()


        # apply filter #
        ################
        # chem is save for global structure
        dout = deepcopy(self.dchem)

        i = 0
        lcas = list(dout.keys())
        imax = len(lcas)
        while i < imax:
            nactive = 0
            nassays = 0
            ninactive = 0

            #if not "activeAssays" in dout[lcas[i]].__dict__ and not "linactive" in dout[lcas[i]].__dict__:
            #    del dout[lcas[i]]
            #    del lcas[i]
            #    imax = imax - 1
            #    continue



            #filter assays active
            ai = 0
            amax = len(list(dout[lcas[i]].activeAssays.keys()))
            while ai < amax:
                nameassays = list(dout[lcas[i]].activeAssays.keys())[ai]
                source = nameassays.split("_")[0]
                nactive = nactive + 1
                nassays = nassays + 1
                #if source in lsourceAssays:
                ai = ai + 1
                #else:
                #    del dout[lcas[i]].activeAssays[dout[lcas[i]].activeAssays.keys()[ai]]
                #    amax = amax - 1


            #filter assays no test
            ai = 0
            amax = len(dout[lcas[i]].notestAssays)
            while ai < amax:
                nameassays = dout[lcas[i]].notestAssays[ai]
                source = nameassays.split("_")[0]
                nassays = nassays + 1
                #if source in lsourceAssays:
                ai = ai + 1
                #else:
                #    del dout[lcas[i]].notestAssays[ai]
                #    amax = amax - 1


            #filter no active test
            ai = 0
            amax = len(dout[lcas[i]].inactiveAssays)
            while ai < amax:
                nameassays = dout[lcas[i]].inactiveAssays[ai]
                source = nameassays.split("_")[0]
                ninactive = ninactive + 1
                nassays = nassays + 1
                #if source in lsourceAssays:
                ai = ai + 1
                #else:
                #    del dout[lcas[i]].inactiveAssays[ai]
                #    amax = amax - 1


            percentageAct = float(nactive + ninactive)/float(nassays)*100.0
            if percentageAct < cutoffActive:
                del dout[lcas[i]]
            i = i + 1


        lassays = dout[list(dout.keys())[0]].notestAssays + dout[list(dout.keys())[0]].inactiveAssays + \
                  list(dout[list(dout.keys())[0]].activeAssays.keys())

        chemfilout = open(pchemfilout, "w")
        chemfilout.write("CAS\t" + "\t".join(lassays) + "\n")
        for CASID in dout.keys():
            chemfilout.write(CASID)
            for assays in lassays:
                if assays in dout[CASID].activeAssays.keys():
                    chemfilout.write("\t" + str(dout[CASID].activeAssays[assays]))
                elif assays in dout[CASID].inactiveAssays:
                    chemfilout.write("\t1000000")
                elif assays in dout[CASID].notestAssays:
                    chemfilout.write("\tNA")
            chemfilout.write("\n")
        chemfilout.close()

        assaysfilout = open(passaysfilout, "w")
        assaysfilout.write("Assays\tGene\n")
        for assays in lassays:
            gene = self.dassays[assays].charac["intended_target_gene_symbol"].upper()
            if gene != "":
                assaysfilout.write(assays + "\t" + self.dassays[assays].charac["intended_target_gene_symbol"].upper() + "\n")
        assaysfilout.close()

        return [pchemfilout, passaysfilout]


    def loadAC50(self, lassaysin=[]):

        fAC50 = open(self.pAC50, "r")
        lchemIC50 = fAC50.readlines()
        fAC50.close()

        if lassaysin == []:
            lassays = lchemIC50[0].strip().replace("\"", "").split(",")
        else:
            lassays = lassaysin

        for chemIC50 in lchemIC50[1:]:
            lChemIC50 = chemIC50.strip().split(",")
            chemID = lChemIC50[0]
            chemID = chemID.replace("\"", "")

            CASID = self.convertIDtoCAS(chemID)

            if CASID != "ERROR":
                self.dchem[CASID].setIC50(lassays, lChemIC50)


    def loadAC50forAssay(self, assaysName, notest):

        if not "dchem" in self.__dict__:
            self.loadChem()
            self.loadAC50()

        dassayout = {}
        for chem in self.dchem.keys():
            if assaysName in self.dchem[chem].notestAssays:
                if notest == 1:
                    dassayout[chem] = "NA"
            elif assaysName in self.dchem[chem].inactiveAssays:
                dassayout[chem] = 1000000
            else:
                dassayout[chem] = float(self.dchem[chem].activeAssays[assaysName])
        return dassayout



    def convertIDtoCAS(self, chemID):

        for CASID in self.dchem.keys():
            if self.dchem[CASID].code == chemID:
                return CASID

        return "ERROR"


    def writebyChemical(self, prout):

        lassays = list(self.dassays.keys())

        for chem in self.dchem.keys():
            pfileAC50 = prout + chem + ".csv"
            fileAC50 = open(pfileAC50, "w")
            fileAC50.write("CASRN\t" + "\t".join(lassays) + "\n")
            fileAC50.write(str(chem))
            for assay in lassays:
                if assay in list(self.dchem[chem].activeAssays.keys()):
                    fileAC50.write("\t" + str(self.dchem[chem].activeAssays[assay]))
                elif assay in self.dchem[chem].inactiveAssays:
                    fileAC50.write("\t1000000")
                else:
                    fileAC50.write("\tNA")
            fileAC50.close()

        return prout


    def writeAssaysResult(self, pfileAC50):


        if path.exists(pfileAC50):
            return pfileAC50
        else:

            lassays = list(self.dassays.keys())

            fileAC50 = open(pfileAC50, "w")
            fileAC50.write("CASRN\t" + "\t".join(lassays) + "\n")

            for chem in self.dchem.keys():
                fileAC50.write(str(chem))
                for assay in lassays:
                    if assay in list(self.dchem[chem].activeAssays.keys()):
                        fileAC50.write("\t" + str(self.dchem[chem].activeAssays[assay]))
                    elif assay in self.dchem[chem].inactiveAssays:
                        fileAC50.write("\t1000000")
                    else:
                        fileAC50.write("\tNA")
                fileAC50.write("\n")
            fileAC50.close()

            return pfileAC50


    def filterFormatAssaysResult(self, pfileAC50, cutoffChemical = 100, log=1, cor=0.9 ):
        runExternalScript.cleanAssayResult(pfileAC50, cutoffChemical, log, cor)
        return






