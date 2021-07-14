from os import system, path, chdir


# have to be fix!!!
def runRCMD(cmd, out = 0, linux=1):
    chdir("./../R/")
    print(cmd)
    if out == 0:
        if linux != 1:
            cmd = "C://Program Files//R//R-3.5.2//bin//Rscript.exe " + cmd
            print(cmd)
        system(cmd)
        output = 0
    else:
        import subprocess
        output = subprocess.check_output(cmd, shell=True)
    chdir("./../py/")
    return output



def cleanAssayResult(pfileAC50, prout, cutoffChemical, cutoffAssays, corval, log):

    pfilout = "%sMassays_%s-%s_%s_log%s.csv"%(prout, cutoffChemical, cutoffAssays, corval, log)
    print(pfilout)
    if path.exists(pfilout):
        return pfilout
    else:
        cmd = "./prepAssay.R " + pfileAC50 + " " + str(cutoffChemical) + " " + str(cutoffAssays) + " " + str(log) + " " + str(corval) + " " + str(prout)
        runRCMD(cmd)

        if path.exists(pfilout):
            return pfilout
        else:
            return "Error"


