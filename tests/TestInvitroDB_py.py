import unittest
import invitroDB_py


class TestInvitroDB_py(unittest.TestCase):

    def test_loadDATA(self):
        
        p_ICE = "/mnt/d/database/invitroDB3.3_7-14-21/ICE_invitroDB3.3_7-14-21/cHTS2021_invitrodb33_20210128.txt"
        p_assays_sum = "/mnt/d/database/invitroDB3.3_7-14-21/EPA_invitroDB-3.3_7-14-21/INVITRODB_V3_3_SUMMARY/assay_annotation_information_invitrodb_v3_3.xlsx"

        cInvitroDB = invitroDB_py.invitroDB_py(p_ICE, p_assays_sum)
        cInvitroDB.load_AssaysAndICE()

        self.assertEqual(cInvitroDB.err, 0)

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

