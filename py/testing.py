import ToxCast



prtest = "./../../trash/"
pchem = prtest + "INVITRODB_V3_1_SUMMARY/Chemical_Summary_190226.csv"
pAC50 = prtest + "INVITRODB_V3_1_SUMMARY/ac50_Matrix_190226.csv"
passays = prtest + "INVITRODB_V3_1_SUMMARY/Assay_Summary_190226.csv"


cToxCast = ToxCast.ToxCast([], prtest, pchem, pAC50, passays)
ltopChem = cToxCast.getTopActive("TOX21_MMP_rhodamine", 10)

print(",".join(ltopChem))
print(ltopChem)

