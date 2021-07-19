from toolboxLib import loadExcelSheet
from .Map import Map

class GeneMap:

    def __init__(self, p_geneMap):
        self.p_geneMap = p_geneMap

    def loadMapping(self):

        # define row i as ki
        d_geneMap = loadExcelSheet(self.p_geneMap, "Sheet 1")

        #organize using the gene symbol
        d_out = {}
        for id in d_geneMap.keys():
            gene_official_symbol = d_geneMap[id]["official_symbol"]

            try:d_out[gene_official_symbol]
            except:
                d_out[gene_official_symbol] = Map(d_geneMap[id])
            
            d_out[gene_official_symbol].l_organism_id.append(d_geneMap[id]["organism_id"])
            d_out[gene_official_symbol].l_track_status.append(d_geneMap[id]["track_status"])
            d_out[gene_official_symbol].l_aeid.append(d_geneMap[id]["aeid"])
            d_out[gene_official_symbol].l_aenm.append(d_geneMap[id]["aenm"])
        
        self.d_geneMap = d_out


