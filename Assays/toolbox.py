import pandas
from re import search


def loadExcelSheet(p_excel, name_sheet, k_head):
    """
    TO DO: Add check duplicate rownames
    """

    d_out = {}
    # load MC list
    data_frame = pandas.read_excel(p_excel, name_sheet, engine='openpyxl')
    data_size = data_frame.shape
    nb_row = data_size[0]
    nb_col = data_size[1]
    l_col = data_frame.columns

    i = 0
    while i < nb_row:
        rowname = data_frame.iloc[i][k_head]
        if not rowname in list(d_out.keys()):
            d_out[rowname] = {}
        j = 0
        while j < nb_col:
            colname = l_col[j]
            if search("Unnamed:", colname):
                j = j + 1
                continue
            else:
                d_out[rowname][colname] = data_frame.iloc[i][l_col[j]]
            j = j + 1
        i = i + 1
    
    return d_out







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




