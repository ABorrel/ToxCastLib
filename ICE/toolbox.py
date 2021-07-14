
def formatLine(linein):
    
    linein = linein.replace("\n", "")
    linenew = ""

    imax = len(linein)
    i = 0
    flagchar = 0
    while i < imax:
        if linein[i] == '"' and flagchar == 0:
            flagchar = 1
        elif linein[i] == '"' and flagchar == 1:
            flagchar = 0

        if flagchar == 1 and linein[i] == ",":
            linenew = linenew + " "
        else:
            linenew = linenew + linein[i]

        i += 1

    linenew = linenew.replace('\"', "")
    return linenew



def loadMatrixToList(pmatrixIn, sep = "\t"):
    
    filin = open(pmatrixIn, "r", encoding="utf8", errors='ignore')
    llinesMat = filin.readlines()
    filin.close()

    return llinesMat

    l_out = []
    line0 = formatLine(llinesMat[0])
    line1 = formatLine(llinesMat[1])
    lheaders = line0.split(sep)
    lval1 = line1.split(sep)

    # case where R written
    if len(lheaders) == (len(lval1) -1):
        lheaders = ["ID"] + lheaders


    i = 0
    while i < len(lheaders):
        if lheaders[i] == "":
            lheaders[i] = "ID"
        i += 1

    i = 1
    imax = len(llinesMat)
    while i < imax:
        lineMat = formatLine(llinesMat[i])
        lvalues = lineMat.split(sep)
        j = 0
        if len(lvalues) != len(lheaders):
            print("ERROR - line: ", i)
            print(lvalues)
            print(lheaders)
        jmax = len(lheaders)
        dtemp = {}
        while j < jmax:
            try:dtemp[lheaders[j]] = lvalues[j]
            except:pass
            j += 1
        l_out.append(dtemp)
        i += 1

    return l_out