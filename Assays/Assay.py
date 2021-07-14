
class Characteristic:
    def __init__(self, d_in):

        self.charac = {}
        self.charac["aid"] = d_in["aid"]
        self.charac["asid"] = d_in["asid"]
        self.charac["assay_name"] = d_in["assay_name"]
        self.charac["assay_desc"] = d_in["assay_desc"]
        self.charac["timepoint_hr"] = d_in["timepoint_hr"]
        self.charac["organism_id"] = d_in["organism_id"]
        self.charac["organism"] = d_in["organism"]
        self.charac["tissue"] = d_in["tissue"]         
        self.charac["cell_format"] = d_in["cell_format"]
        self.charac["cell_free_component_source"] = d_in["cell_free_component_source"]
        self.charac["cell_short_name"] = d_in["cell_short_name"]
        self.charac["cell_growth_mode"] = d_in["cell_growth_mode"]  
        self.charac["assay_footprint"] = d_in["assay_footprint"]
        self.charac["assay_format_type"] = d_in["assay_format_type"]
        self.charac["assay_format_type_sub"] = d_in["assay_format_type_sub"]
        self.charac["content_readout_type"] = d_in["content_readout_type"] 
        self.charac["dilution_solvent"] = d_in["dilution_solvent"]
        self.charac["dilution_solvent_percent_max"] = d_in["dilution_solvent_percent_max"] 




class Component:

    def __init__(self, d_in):

        self.charac = {}       
        self.charac["technological_target_type"] = d_in["technological_target_type"]
        self.charac["technological_target_type_sub"] = d_in["technological_target_type_sub"]
        self.charac["detection_technology"] = d_in["detection_technology"]
        self.charac["signal_direction_type"] = d_in["signal_direction_type"]
        self.charac["key_assay_reagent_type"] = d_in["key_assay_reagent_type"]
        self.charac["key_assay_reagent"] = d_in["key_assay_reagent"]
        self.charac["assay_design_type_sub"] = d_in["assay_design_type_sub"]
        self.charac["biological_process_target"] = d_in["biological_process_target"]
        self.charac["detection_technology_type"] = d_in["detection_technology_type"]
        self.charac["detection_technology_type_sub"] = d_in["detection_technology_type_sub"]
        self.charac["acid"] = d_in["acid"]
        self.charac["aid"] = d_in["aid"]
        self.charac["assay_component_name"] = d_in["assay_component_name"]
        self.charac["assay_component_desc"] = d_in["assay_component_desc"]
        self.charac["assay_component_target_desc"] = d_in["assay_component_target_desc"]
        self.charac["parameter_readout_type"] = d_in["parameter_readout_type"]
        self.charac["parameter_readout_type"] = d_in["parameter_readout_type"]
        self.charac["assay_design_type"] = d_in["assay_design_type"]


