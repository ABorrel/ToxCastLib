from Assays import Assays
from ICE import ICE
from GeneMap import GeneMap


class ToxCastLib:

    def __init__(self, p_ICE, p_assays_summary, p_geneMap):
        
        # path with the database
        self.p_ICE = p_ICE
        self.p_assays_summary = p_assays_summary
        self.p_geneMap = p_geneMap
        
        # initialize classes
        self.c_Assays = Assays.Assays(self.p_assays_summary)
        self.c_ICE = ICE.ICE(self.p_ICE)
        self.c_geneMap = GeneMap.GeneMap(self.p_geneMap)
        self.err = 0

    def load_AssaysAndICEAndGeneMap(self):
        self.c_Assays.loadAll()
        self.c_ICE.load_ICE()
        self.c_geneMap.loadMapping()


    def get_EndpointByGene(self, l_genes):
        """
        input: a list of genes
        return: a list of endpoints ids
        genes need to be in the official symbol name (in MAJ)
        """
        if not "d_geneMap" in self.c_geneMap.__dict__:
            self.c_geneMap.loadMapping()

        l_out = []
        for gene in l_genes:
            l_out = l_out + self.c_geneMap.d_geneMap[gene].l_aeid
        
        return l_out


    def get_aenmFromaied(self, aeid):

        if not "c_Endpoint" in self.c_Assays.__dict__:
            self.c_Assays.load_aeid()

        return self.c_Assays.c_Endpoint[aeid].charac["assay_component_endpoint_name"]



    def get_resultTableFromGenes(self, l_genes, pr_out):

        d_out = {}
        l_aeid = self.get_EndpointByGene(l_genes)
        l_chem_tested = []
        for aeid in l_aeid:
            aenm = self.get_aenmFromaied(aeid)
            d_out[aenm] = self.c_ICE.get_resultsByEndpoints(aenm)
            l_chem_tested = l_chem_tested + d_out[aenm].CASRN
       
        # merge results
        l_chem_tested = list(set(l_chem_tested))

        p_filout = pr_out + "-".join(l_genes) + ".csv"
        filout = open(p_filout, "w")
        filout.write("CASRN\tChemical.name\t%s\n"%("\t".join(["%s\t%s_unit"%(aenm, aenm) for aenm in d_out.keys()])))

        for chem in l_chem_tested:
            w = []
            for aenm in d_out.keys():
                try: 
                    i_chem = d_out[aenm].CASRN.index(chem)
                except:
                    i_chem = "NA"
                
                if i_chem != "NA":
                    w.append(d_out[aenm].Response[i_chem])
                    w.append(d_out[aenm].ResponseUnit[i_chem])
                else:
                    w.append("NT")
                    w.append("NA")
            
            filout.write(chem + "\t" + self.c_ICE.chemicals[chem].name + "\t" + "\t".join(w) + "\n")
        filout.close()
        return p_filout


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
