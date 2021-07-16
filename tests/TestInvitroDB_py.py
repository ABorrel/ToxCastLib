from os import path

import unittest
import invitroDB_py

p_ICE = "/mnt/d/database/invitroDB3.3_7-14-21/ICE_invitroDB3.3_7-14-21/cHTS2021_invitrodb33_20210128.txt"
p_assays_sum = "/mnt/d/database/invitroDB3.3_7-14-21/EPA_invitroDB-3.3_7-14-21/INVITRODB_V3_3_SUMMARY/assay_annotation_information_invitrodb_v3_3.xlsx"
p_gene_mapping = "/mnt/d/database/invitroDB3.3_7-14-21/EPA_invitroDB-3.3_7-14-21/INVITRODB_V3_3_SUMMARY/gene_target_information_invitrodb_v3_3.xlsx"


class TestInvitroDB_py(unittest.TestCase):
    """
    def test_loadDATA(self):
        cInvitroDB = invitroDB_py.invitroDB_py(p_ICE, p_assays_sum, p_gene_mapping)
        cInvitroDB.load_AssaysAndICEAndGeneMap()

        self.assertEqual(cInvitroDB.err, 0)
    
    def test_findEndpoints(self):

        cInvitroDB = invitroDB_py.invitroDB_py(p_ICE, p_assays_sum, p_gene_mapping)
        l_out = cInvitroDB.get_EndpointByGene(["CYP19A1"])
        self.assertEqual(l_out, [319, 320, 767])
    
    def test_aeidToaenm(self):

        cInvitroDB = invitroDB_py.invitroDB_py(p_ICE, p_assays_sum, p_gene_mapping)
        name_endpoint = cInvitroDB.get_aenmFromaied(319)
        print(name_endpoint)
        self.assertEqual(name_endpoint, "NVS_ADME_hCYP19A1")

    """

    def test_getAssaysResultsFromGene(self):

        cInvitroDB = invitroDB_py.invitroDB_py(p_ICE, p_assays_sum, p_gene_mapping)
        p_out = cInvitroDB.get_resultTableFromGenes(["CYP19A1"], "/mnt/c/Users/AlexandreBorrel/research/development/ToxCast_lib/sources/tests/")

        self.assertEqual(path.exists(p_out), True)

if __name__ == '__main__':
    unittest.main()



#import ToxCast



#prtest = "./../../trash/"
#pchem = prtest + "INVITRODB_V3_1_SUMMARY/Chemical_Summary_190226.csv"
#pAC50 = prtest + "INVITRODB_V3_1_SUMMARY/ac50_Matrix_190226.csv"
#passays = prtest + "INVITRODB_V3_1_SUMMARY/Assay_Summary_190226.csv"


#cToxCast = ToxCast.ToxCast([], prtest, pchem, pAC50, passays)
#ltopChem = cToxCast.getTopActive("TOX21_MMP_rhodamine", 10)

#print(",".join(ltopChem))
#print(ltopChem)

