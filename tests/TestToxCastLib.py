from os import path

import unittest

from sklearn.metrics import coverage_error
from ToxCastLib import ToxCastLib


p_ICE = "/mnt/d/database/invitroDB3.3_7-14-21/ICE_invitroDB3.3_7-14-21/cHTS2021_invitrodb33_20210128.txt"
p_assays_sum = "/mnt/d/database/invitroDB3.3_7-14-21/EPA_invitroDB-3.3_7-14-21/INVITRODB_V3_3_SUMMARY/assay_annotation_information_invitrodb_v3_3.xlsx"
p_gene_mapping = "/mnt/d/database/invitroDB3.3_7-14-21/EPA_invitroDB-3.3_7-14-21/INVITRODB_V3_3_SUMMARY/gene_target_information_invitrodb_v3_3.xlsx"


class TestToxCastLib(unittest.TestCase):
    
    """def test_loadDATA(self):
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        cInvitroDB.load_AssaysAndICEAndGeneMap()
        self.assertEqual(cInvitroDB.err, 0)
    
    def test_findEndpoints(self):

        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        l_out = cInvitroDB.get_EndpointByGene(["CYP19A1"])
        self.assertEqual(l_out, [319, 320, 767])
    
    def test_aeidToaenm(self):

        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        name_endpoint = cInvitroDB.get_aenmFromaied(319)
        print(name_endpoint)
        self.assertEqual(name_endpoint, "NVS_ADME_hCYP19A1")

    def test_getAssaysResultsFromGene(self):

        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        p_out = cInvitroDB.get_resultTableFromGenes(["CYP19A1"], "/mnt/c/Users/AlexandreBorrel/research/development/ToxCastLib/sources/tests/")
        self.assertEqual(path.exists(p_out), True)
    
    def test_getToxCastResultByChem(self):
        
        CASRN = "91-94-1"
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        result_ToxCast = cInvitroDB.get_ToxCastResultByChem(CASRN)
        self.assertEqual(type(result_ToxCast), dict)
    
    def test_getCoverageAssayTestedByChem(self):

        CASRN = "60-35-5"
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        d_coverage = cInvitroDB.get_coverageTestedAssayByChem(CASRN)
        print(d_coverage)
        self.assertEqual(int(d_coverage["coverage"]), 0)"""
    
    
    def test_get_listAllEndpoint(self):
        
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        l_endpoint = cInvitroDB.get_listAllEndpoint()

        self.assertEqual(type(l_endpoint), list)
       
    def test_get_listAllAssayFunctionType(self):
            
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        l_type = cInvitroDB.get_listAllAssayFunctionType()

        self.assertEqual(type(l_type), list)
        
    def test_get_aeidByNnameEndpoint(self):
       
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        aeid = cInvitroDB.get_aeidByNnameEndpoint("NCCT_MITO_basal_resp_rate_OCR_up")
        self.assertEqual(aeid, 2443) 
        
    def test_get_AllToxCastResultByAssay(self):
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        d_mapped = cInvitroDB.get_AllToxCastResultByAssay("./tests/mapassay.csv")
        
        self.assertEqual(type(d_mapped), dict)
    
    def test_get_AllToxCastResultByAssay(self):
        cInvitroDB = ToxCastLib.ToxCastLib(p_ICE, p_assays_sum, p_gene_mapping)
        d_empty = cInvitroDB.get_KCByNnameEndpoint("NCCT_MITO_basal_resp_rate_OCR_up")
        d_test = cInvitroDB.get_KCByNnameEndpoint("TOX21_PR_BLA_Agonist_viability")
        
        self.assertEqual(d_test, {'aeid': 2124, 'aenm': 'TOX21_PR_BLA_Agonist_viability', 'Characteristic #': 10, 'Description': 'Alters cell proliferation, cell death or nutrient supply'})

if __name__ == '__main__':
    unittest.main()

