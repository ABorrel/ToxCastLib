
class Assay:
    def __init__(self, lelem):


        self.charac = {}

        if len(lelem) == 84:
            self.charac["aid"] = lelem[0]
            self.charac["acid"] = lelem[1]
            self.charac["aeid"] = lelem[2]
            self.charac["asid"] = lelem[3]
            self.charac["assay_source_name"] = lelem[4]
            self.charac["assay_source_long_name"] = lelem[5]
            self.charac["assay_source_desc"] = lelem[6]
            self.charac["assay_name"] = lelem[7]
            self.charac["assay_desc"] = lelem[8]
            self.charac["timepoint_hr"] = lelem[9]
            self.charac["organism_id"] = lelem[10]
            self.charac["organism"] = lelem[11]
            self.charac["tissue"] = lelem[12]
            self.charac["cell_format"] = lelem[13]
            self.charac["cell_free_component_source"] = lelem[14]
            self.charac["cell_short_name"] = lelem[15]
            self.charac["cell_growth_mode"] = lelem[16]
            self.charac["assay_footprint"] = lelem[17]
            self.charac["assay_format_type"] = lelem[18]
            self.charac["assay_format_type_sub"] = lelem[19]
            self.charac["content_readout_type"] = lelem[20]
            self.charac["dilution_solvent"] = lelem[21]
            self.charac["dilution_solvent_percent_max"] = lelem[22]
            self.charac["assay_component_name"]  = lelem[23]
            self.charac["assay_component_desc"]  = lelem[24]
            self.charac["assay_component_target_desc"]  = lelem[25]
            self.charac["parameter_readout_type"] = lelem[26]
            self.charac["assay_design_type"] = lelem[27]
            self.charac["assay_design_type_sub"] = lelem[28]
            self.charac["biological_process_target"] = lelem[29]
            self.charac["detection_technology_type"] = lelem[30]
            self.charac["detection_technology_type_sub"] = lelem[31]
            self.charac["detection_technology"] = lelem[32]
            self.charac["signal_direction_type"] = lelem[33]
            self.charac["key_assay_reagent_type"] = lelem[34]
            self.charac["key_assay_reagent"] = lelem[35]
            self.charac["technological_target_type"] = lelem[36]
            self.charac["technological_target_type_sub"] = lelem[37]
            self.charac["assay_component_endpoint_name"] = lelem[38]
            self.charac["assay_component_endpoint_desc"] = lelem[39]
            self.charac["assay_function_type"] = lelem[40]
            self.charac["normalized_data_type"] = lelem[41]
            self.charac["analysis_direction"] = lelem[42]
            self.charac["burst_assay"] = lelem[43]
            self.charac["key_positive_control"] = lelem[44]
            self.charac["signal_direction"] = lelem[45]
            self.charac["intended_target_type"] = lelem[46]
            self.charac["intended_target_type_sub"] = lelem[47]
            self.charac["intended_target_family"] = lelem[48]
            self.charac["intended_target_family_sub"] = lelem[49]
            self.charac["fit_all"] = lelem[50]
            self.charac["intended_target_gene_id"] = lelem[51]
            self.charac["intended_target_entrez_gene_id"] = lelem[52]
            self.charac["intended_target_official_full_name"] = lelem[53]
            self.charac["intended_target_gene_name"] = lelem[54]
            self.charac["intended_target_official_symbol"] = lelem[55]
            self.charac["intended_target_gene_symbol"] = lelem[56]
            self.charac["intended_target_description"] = lelem[57]
            self.charac["intended_target_uniprot_accession_number"] = lelem[58]
            self.charac["intended_target_organism_id"] = lelem[59]
            self.charac["intended_target_track_status"] = lelem[60]
            self.charac["technological_target_gene_id"] = lelem[61]
            self.charac["technological_target_entrez_gene_id"] = lelem[62]
            self.charac["technological_target_official_full_name"] = lelem[63]
            self.charac["technological_target_gene_name"] = lelem[64]
            self.charac["technological_target_official_symbol"] = lelem[65]
            self.charac["technological_target_gene_symbol"] = lelem[66]
            self.charac["technological_target_description"] = lelem[67]
            self.charac["technological_target_uniprot_accession_number"] = lelem[68]
            self.charac["technological_target_organism_id"] = lelem[69]
            self.charac["technological_target_track_status"] = lelem[70]
            self.charac["citations_citation_id"] = lelem[71]
            self.charac["citations_pmid"] = lelem[72]
            self.charac["citations_doi"] = lelem[73]
            self.charac["citations_other_source"] = lelem[74]
            self.charac["citations_other_id"] = lelem[75]
            self.charac["citations_citation"] = lelem[76]
            self.charac["citations_title"] = lelem[77]
            self.charac["citations_author"] = lelem[78]
            self.charac["citations_url"] = lelem[79]
            self.charac["reagent_arid"] = lelem[80]
            self.charac["reagent_reagent_name_value"] = lelem[81]
            self.charac["reagent_reagent_name_value_type"] = lelem[82]
            self.charac["reagent_culture_or_assay"] = lelem[83]

        self.name = lelem[2]
