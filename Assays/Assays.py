from toolboxLib import loadExcelSheet
from .Assay import Characteristic, Component, Endpoint


class Assays:

    """3 levels of summary
        - aid with onlu assay name
        - acid with component
        - endpoint
    """

    def __init__(self, p_assays_sum):

        self.p_assay_sum = p_assays_sum
    

    def loadAll(self):
        """
        Load all of the element in the summary
        """

        self.load_aid()
        self.load_acid()
        self.load_aeid

    def load_aid(self):
        """
        Load first level of assays name and charac
        Add .charac key
        """
        d_Assay_xlx = loadExcelSheet(self.p_assay_sum, "assay", "aid")
        self.c_Assay = {}
        for aid in d_Assay_xlx.keys():
            cAssay = Characteristic(d_Assay_xlx[aid])
            self.c_Assay[aid] = cAssay


    def load_acid(self):
        """
        Add component level
        Add .comp key
        Do not need to load all level to use
        """
        d_comp_xlx = loadExcelSheet(self.p_assay_sum, "assay.component", "acid")
        self.c_Comp = {}
        for acid in d_comp_xlx.keys():
            cComp = Component(d_comp_xlx[acid])
            self.c_Comp[acid] = cComp


    def load_aeid(self):
        """
        Load endpoint 
        add .endpoint in key
        Do not need to load all level to be used
        """
        d_end_xlx = loadExcelSheet(self.p_assay_sum, "assay.component.endpoint", "aeid")
        self.c_Endpoint = {}
        for aeid in d_end_xlx.keys():
            cEnd = Endpoint(d_end_xlx[aeid])
            self.c_Endpoint[aeid] = cEnd

