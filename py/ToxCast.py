from copy import deepcopy
from os import path

import Assays
import ChemCAS
import runExternalScript

# define the dataset folder
PR_DATA = "/home/borrela2/data/"


def fromatAssaysBlock(AssaysBlock):

    # format split \n
    AssaysBlock = list(AssaysBlock)
    i = 0
    imax = len(AssaysBlock)
    flagopen = 0
    while i < imax:
        if AssaysBlock[i] == "\"" and flagopen == 0:
            flagopen = 1
        elif AssaysBlock[i] == "\"" and flagopen == 1:
            flagopen = 0

        if flagopen == 1 and AssaysBlock[i] == "\n":
            AssaysBlock[i] = " "
        elif flagopen == 1 and AssaysBlock[i] == ",":
            AssaysBlock[i] = " "

        i = i + 1

    llinesAssays = "".join(AssaysBlock).split("\n")

    lout = []
    for lineAssays in llinesAssays[1:]:
        # remove extra " in the line
        lineAssays = lineAssays.replace("\"", "")
        lelem = lineAssays.strip().split(",")
        if len(lelem) == 84:
            lout.append(lelem)


    return lout






class ToxCast:

    def __init__(self, lsources, prresults):

        self.pchem = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/Chemical_Summary_190226.csv"
        self.pAC50 = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/ac50_Matrix_190226.csv"
        self.passays = PR_DATA + "invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/Assay_Summary_190226.csv"
        self.lsource = lsources
        self.prresults = prresults
        self.version = "InVitroDB 3.1"
        self.update = "March-2019"


    def loadAssays(self):

        fassays = open(self.passays, "r", encoding="utf8", errors='ignore')
        blockassays = fassays.read()
        fassays.close()

        llassays = fromatAssaysBlock(blockassays)
        dout = {}
        for lassay in llassays:
            cassays = Assays.Assay(lassay)
            nameAssay = cassays.charac["assay_component_endpoint_name"]

            if self.lsource != []:
                #print cassys.charac["assay_source_name"]
                if cassays.charac["assay_source_name"] in self.lsource:
                    dout[nameAssay] = cassays
            else:
                dout[nameAssay] = cassays

        self.dassays = dout


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
            lassays = lchemIC50[0].strip().split(",")
        else:
            lassays = lassaysin

        for chemIC50 in lchemIC50[1:]:
            lChemIC50 = chemIC50.strip().split(",")
            chemID = lChemIC50[0]
            chemID = chemID.replace("\"", "")

            CASID = self.convertIDtoCAS(chemID)

            if CASID != "ERROR":
                self.dchem[CASID].setIC50(lassays, lChemIC50)



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






