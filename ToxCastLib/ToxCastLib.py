from pickle import FALSE, TRUE
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
        
        # filter apply on function to select part of the results
        self.l_type_assay_toselect = []
        self.l_assay_toselect = []
        

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

    def get_aeidByNnameEndpoint(self, endpoint_in):
        
        if not "c_Endpoint" in self.c_Assays.__dict__:
            self.c_Assays.load_aeid()
        
        for aeid in self.c_Assays.c_Endpoint.keys():
            endpoint = self.c_Assays.c_Endpoint[aeid].charac["assay_component_endpoint_name"]
            
            if endpoint == endpoint_in:
                return aeid
        
        return  0

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
    
    def get_coverageTestedAssayByChem(self, CASRN, store=FALSE):
        """Function used to compute the coverage of assay tested

        Args:
            CASRN (str): [description]
            store (bool, optional): Use to sore the mapping.

        Returns:
            [dictionnary]: dictionnary with the number of assays tested and non tested with the coverage score
        """
        d_toxcast = self.get_ToxCastResultByChem(CASRN, store) 
        coverage = float(len(d_toxcast["List tested assays"]))/(len(d_toxcast["List tested assays"]) + len(d_toxcast["List no tested assays"]))
        d_out = {"Nb assays tested":len(d_toxcast["List tested assays"]), "Nb no tested":  len(d_toxcast["List no tested assays"]), "coverage": coverage}
        return d_out

    def get_listAllEndpoint(self):
        
        l_out = []
        
        if not "c_Endpoint" in self.c_Assays.__dict__:
            self.c_Assays.load_aeid()
        
        for aeid in self.c_Assays.c_Endpoint.keys():
            endpoint = self.c_Assays.c_Endpoint[aeid].charac["assay_component_endpoint_name"]
            l_out.append(endpoint) 
        
        return l_out
    
    def get_listAllAssayFunctionType(self):
        l_out = []
        
        if not "c_Endpoint" in self.c_Assays.__dict__:
            self.c_Assays.load_aeid()
        
        for aeid in self.c_Assays.c_Endpoint.keys():
            function_type = self.c_Assays.c_Endpoint[aeid].charac["assay_function_type"]
            if not function_type in l_out:
                l_out.append(function_type) 
        
        return l_out
        
    def get_ToxCastResultByChem(self, CASRN, store = False):
        """
        Args:
            CASRN (str): CASRN of chemical of interest 
            store (bool, optional): Store create a new variable that store the mapping. Defaults to False.
        Return:
            Dictionnary with list of AC50, assays tested, list of unit and assays no tested
        """
        # need to extract all assays with the chemicals
        # load ICE
        if not "resultEndpoint" in self.c_ICE.__dict__:
            self.c_ICE.load_ICE()

        # define a variable to store mapping
        if store == True:
            if not "d_chem_mapped" in self.__dict__:
                self.d_chem_mapped = {}
            
            if CASRN in list(self.d_chem_mapped):
                return self.d_chem_mapped[CASRN]
        
        d_out = {"List tested assays":[], "List AC50 or QC":[], "List no tested assays":[], "Unit":[]}
        for endpoint in self.c_ICE.resultEndpoint.keys():
            if self.l_assay_toselect != [] and not endpoint in self.l_assay_toselect:
                continue
            if self.l_type_assay_toselect != []:
                aeid = self.get_aeidByNnameEndpoint(endpoint)
                function_type = self.c_Assays.c_Endpoint[aeid].charac["assay_function_type"]
                if not function_type in self.l_type_assay_toselect:
                    continue
            if CASRN in self.c_ICE.resultEndpoint[endpoint].CASRN:
                i_CASRN = self.c_ICE.resultEndpoint[endpoint].CASRN.index(CASRN)
                d_out["List AC50 or QC"].append(self.c_ICE.resultEndpoint[endpoint].Response[i_CASRN])
                d_out["List tested assays"].append(endpoint)
                d_out["Unit"].append(self.c_ICE.resultEndpoint[endpoint].ResponseUnit[i_CASRN])
            else:
                d_out["List no tested assays"].append(endpoint)
        
        if store == TRUE:
            self.d_chem_mapped[CASRN] = d_out
        
        return d_out