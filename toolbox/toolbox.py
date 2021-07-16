import pandas
from re import search


def loadMatrixToList(pmatrixIn):
    """
    Uptimize to load file fast and not do the parsing before usefull
    """

    filin = open(pmatrixIn, "r", encoding="utf8", errors='ignore')
    llinesMat = filin.readlines()
    filin.close()

    return llinesMat





def loadExcelSheet(p_excel, name_sheet, k_head = None):
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
        if k_head == None:
            rowname = i
        else:
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
