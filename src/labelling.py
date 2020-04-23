import cemo.const

def get_region_label(region_idx):
    """ Returns the region label associated with a region index. """
    return cemo.const.REGION[region_idx]

def get_region_for_zone(zone_idx):
    """ Returns the region index that a given zone falls into. """
    for pair in cemo.const.ZONES_IN_REGIONS:
        if pair[1] == zone_idx:
            return pair[0]
    return None

def get_region_label_for_zone(zone_idx):
    """ Returns the region label that a given zone index falls into. """
    region_idx = get_region_for_zone(zone_idx)
    return get_region_label(region_idx)

def get_region_label_for_zone_label(zone_label):
    """Returns the regiuon label that a given zone label falls into. """
    # Get the zone idx
    idx = None
    for zone_idx in cemo.const.ZONE:
        if cemo.const.ZONE[zone_idx] == zone_label:
            idx = zone_idx
            break

    # Now look up the retion label
    return get_region_label_for_zone(idx)


def get_zone_label(zone_idx):
    """ Returns a zone label associated with each zone index. """
    return cemo.const.ZONE[zone_idx]

def get_tech_label(gen_idx):
    return cemo.const.TECH_TYPE[gen_idx]


GAS_GENS = [
'ccgt',
'ccgt_ccs',
'ocgt',
'recip_engine',
'gas_thermal',
]

COAL_GENS = [
'coal_sc',
'coal_sc_ccs',
'brown_coal_sc',
'brown_coal_sc_ccs',
'coal_sc_new']

PV_GENS = [
    
'solar_pv_dat',
'solar_pv_ffp',
'solar_pv_sat',

]

WIND_GENS = [
    
'wind',
'wind_h',

]

CST_GENS = [
    
    'cst_6h',
  
    'cst_3h',
    'cst_12h',
   
]

STORAGE_GENS = [
    'phes_6h',
    'battery_2h',
    'pumps',
    'phes_168h',
    'phes_3h',
    'phes_12h',
    'battery_1h',
    'battery_3h',
]

BIOMASS_GENS = ['biomass',]

HYDRO_GENS = ['hydro',]

def get_tech_classification(gen_label):
    """Provides a broader flassification for a generator label type, out of gas, coal, pv, wind, cst, storage, biomass or traditional_hydro"""
    if gen_label in HYDRO_GENS:
        return 'conventional_hydro'
    elif gen_label in WIND_GENS:
        return 'wind'
    elif gen_label in PV_GENS:
        return 'pv'
    elif gen_label in STORAGE_GENS:
        return 'storage'
    elif gen_label in GAS_GENS:
        return 'gas'
    elif gen_label in COAL_GENS:
        return 'coal'
    elif gen_label in CST_GENS:
        return 'cst'
    elif gen_label in BIOMASS_GENS:
        return 'biomass'
    else:
        raise Exception('ERROR: Could not classify. Check labelling.py and ensure gen label is in a class.', gen_label)

