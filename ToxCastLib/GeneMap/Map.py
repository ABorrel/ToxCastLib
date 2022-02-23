

class Map:

    def __init__(self, d_in):
        
        self.gene_id = d_in["gene_id"]
        self.entrez_gene_id = d_in["entrez_gene_id"]
        self.official_full_name = d_in["official_full_name"]
        self.gene_name = d_in["gene_name"]
        self.official_symbol = d_in["official_symbol"]
        self.gene_symbol = d_in["gene_symbol"]
        self.uniprot_accession_number = d_in["uniprot_accession_number"]
        self.l_organism_id = []
        self.l_track_status = []
        self.l_aeid = []
        self.target_id = d_in["target_id"]
        self.l_aenm = []
