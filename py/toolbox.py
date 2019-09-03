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




