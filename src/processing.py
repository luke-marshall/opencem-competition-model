from .labelling import get_region_label, get_region_for_zone, get_region_label_for_zone, get_region_label_for_zone_label, get_zone_label, get_tech_label

TIME_PERIOD_HRS = 1.0

from . import labelling

def process_unserved(unserved, timeseries_dict):
    for dp in unserved:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        dt = dp['index'][1]
        unserved = dp['value']
        
        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['unserved'] = dp['value']
    
    return timeseries_dict

def process_surplus(surplus, timeseries_dict):
    for dp in surplus:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        dt = dp['index'][1]
        surplus = dp['value']
        

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['surplus'] = dp['value']
    
    return timeseries_dict


def process_region_net_demand(region_net_demand):
    regional_demand_timeseries = {}
    for dp in region_net_demand:
        # print(dp)
        region = get_region_label(dp['index'][0])
        dt = dp['index'][1]
        region_net_demand = dp['value']

        regional_demand_timeseries[dt] = regional_demand_timeseries[dt] if dt in regional_demand_timeseries else {}
        regional_demand_timeseries[dt][region] = dp['value']
    
    return regional_demand_timeseries


def process_gen_cap_factor(gen_cap_factor, timeseries_dict):
    for dp in gen_cap_factor:
        # print(dp)
        
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        gen_cap_factor = dp['value']
        

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['gen_cap_factor'] = timeseries_dict[dt][zone]['gen_cap_factor'] if 'gen_cap_factor' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['gen_cap_factor'][tech] = dp['value']
    
    return timeseries_dict


def process_hyb_cap_factor(hyb_cap_factor, timeseries_dict):
    for dp in hyb_cap_factor:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        hyb_cap_factor = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['hyb_cap_factor'] = timeseries_dict[dt][zone]['hyb_cap_factor'] if 'hyb_cap_factor' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['hyb_cap_factor'][tech] = dp['value']
    
    return timeseries_dict

def process_intercon_cap_op(intercon_cap_op):
    """Retrieves a list of intercon_cap_op values from the OpenCEM output and returns a lookup table that gives the capacity of each interconnector.  """
    intercon_cap_lookup = {}
    for dp in intercon_cap_op:
        # print(dp)
        source = get_zone_label(dp['index'][0])
        dest = get_zone_label(dp['index'][1])
        intercon_cap_lookup[source] = intercon_cap_lookup[source] if source in intercon_cap_lookup else {}
        intercon_cap_lookup[source][dest] = dp['value']
    
    return intercon_cap_lookup

def process_cap_op(cap_op):
    """Retrieves a list of cap_op values from the OpenCEM output and returns a lookup table of zones, technology types to get operating capacity of that tech for that zone.  """
    gen_cap_lookup = {}
    for dp in cap_op:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        gen_cap_lookup[zone] = gen_cap_lookup[zone] if zone in gen_cap_lookup else {}
        gen_cap_lookup[zone][tech] = dp['value']
    
    return gen_cap_lookup

def process_gen_disp(gen_disp, timeseries_dict):
    for dp in gen_disp:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        gen_disp = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['gen_disp'] = timeseries_dict[dt][zone]['gen_disp'] if 'gen_disp' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['gen_disp'][tech] = gen_disp
    
    return timeseries_dict

def process_hyb_disp(hyb_disp, timeseries_dict):
    for dp in hyb_disp:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        hyb_disp = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['hyb_disp'] = timeseries_dict[dt][zone]['hyb_disp'] if 'hyb_disp' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['hyb_disp'][tech] = hyb_disp
    
    return timeseries_dict

def process_stor_disp(stor_disp, timeseries_dict):
    for dp in stor_disp:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        stor_disp = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['stor_disp'] = timeseries_dict[dt][zone]['stor_disp'] if 'stor_disp' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['stor_disp'][tech] = stor_disp
    
    return timeseries_dict


def process_stor_level(stor_level, timeseries_dict):
    for dp in stor_level:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        stor_level = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['stor_level'] = timeseries_dict[dt][zone]['stor_level'] if 'stor_level' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['stor_level'][tech] = stor_level
    
    return timeseries_dict


def process_hyb_level(hyb_level, timeseries_dict):
    for dp in hyb_level:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        hyb_level = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['hyb_level'] = timeseries_dict[dt][zone]['hyb_level'] if 'hyb_level' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['hyb_level'][tech] = hyb_level
    
    return timeseries_dict

def process_hyb_charge(hyb_charge, timeseries_dict):
    for dp in hyb_charge:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        hyb_charge = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['hyb_charge'] = timeseries_dict[dt][zone]['hyb_charge'] if 'hyb_charge' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['hyb_charge'][tech] = hyb_charge
    
    return timeseries_dict


def process_stor_charge(stor_charge, timeseries_dict):
    """Storage charge appears to be <the amount charged> not hte level of charge - that's 'storage level'. """
    for dp in stor_charge:
        # print(dp)
        zone = get_zone_label(dp['index'][0])
        tech = get_tech_label(dp['index'][1])
        dt = dp['index'][2]
        stor_charge = dp['value']

        timeseries_dict[dt] = timeseries_dict[dt] if dt in timeseries_dict else {}
        timeseries_dict[dt][zone] = timeseries_dict[dt][zone] if zone in timeseries_dict[dt] else {}
        timeseries_dict[dt][zone]['stor_charge'] = timeseries_dict[dt][zone]['stor_charge'] if 'stor_charge' in timeseries_dict[dt][zone] else {}
        timeseries_dict[dt][zone]['stor_charge'][tech] = stor_charge
    
    return timeseries_dict




def process_zonal_timeseries(timeseries_dict, gen_cap_lookup, hyb_cap_lookup, stor_cap_lookup, regional_demand_timeseries):
    """ Processes the timeseries built from raw output data. Returns a regionally aggregated timeseries, with the intention of applying NERSI. """
    regional_timeseries = {}

    for dt in timeseries_dict:
        # print("\n\n", dt)
        regional_timeseries[dt] = {}
        for zone in timeseries_dict[dt]:
            # print("\nZone", zone)
            # Add appropriate dicts to the timeseries if not available
            region = get_region_label_for_zone_label(zone)
            # print(region)
            if region not in regional_timeseries[dt]:

                regional_timeseries[dt][region] =  {
                    'total_demand_MW': regional_demand_timeseries[dt][region]/ TIME_PERIOD_HRS,
                    'total_available_capacity_MW': 0,

                    'conventional_hydro_available_MW':0,
                    'wind_available_MW':0,
                    'pv_available_MW':0,
                    'storage_available_MW':0,
                    'gas_available_MW':0,
                    'coal_available_MW':0,
                    'cst_available_MW':0,
                    'biomass_available_MW':0,
                    
                    
                }

            # Calculate the available capacity of generators
            if 'gen_cap_factor' in timeseries_dict[dt][zone]:
                for g in timeseries_dict[dt][zone]['gen_cap_factor']:
                    
                    cap_factor = timeseries_dict[dt][zone]['gen_cap_factor'][g]
                    total_capacity_MW = gen_cap_lookup[zone][g]
                    total_available_capacity_MW = cap_factor * total_capacity_MW
                    dispatched_MWh = timeseries_dict[dt][zone]['gen_disp'][g]
                    dispatched_MW = dispatched_MWh / TIME_PERIOD_HRS
                    spare_capacity_MW = total_available_capacity_MW - dispatched_MW
                    # print(g, cap_factor, total_capacity_MW, total_available_capacity_MW, dispatched_MW, spare_capacity_MW)
                    regional_timeseries[dt][region]['total_available_capacity_MW'] += total_available_capacity_MW
                    # regional_timeseries[dt][region]['spare_capacity_MW'] += spare_capacity_MW
                    # regional_timeseries[dt][region]['dispatched_MW'] += dispatched_MW

                    classification = labelling.get_tech_classification(g)
                    regional_timeseries[dt][region][classification+'_available_MW'] += total_available_capacity_MW
                    
                
            # Calculate the total available capacity of 'hybrid' generators (ie. concentrating solar thermal)
            # Strategy here is to derate the nameplate cap by the cap factor to find available solar coming through, then add any stored available energy, and max it with the nameplate cap. 
            if 'hyb_cap_factor' in timeseries_dict[dt][zone]:
                for g in timeseries_dict[dt][zone]['hyb_cap_factor']:
                    # print(g)
                    cap_factor = timeseries_dict[dt][zone]['hyb_cap_factor'][g]
                    total_nameplate_capacity_MW = hyb_cap_lookup[zone][g]
                    total_instantaneous_capacity_MW = cap_factor * total_nameplate_capacity_MW
                    total_stored_capacity_MW = timeseries_dict[dt][zone]['hyb_level'][g] / TIME_PERIOD_HRS
                    total_available_capacity_MW = min(total_instantaneous_capacity_MW + total_stored_capacity_MW, total_nameplate_capacity_MW)
                    dispatched_MWh = timeseries_dict[dt][zone]['hyb_disp'][g]
                    dispatched_MW = dispatched_MWh / TIME_PERIOD_HRS
                    spare_capacity_MW = total_available_capacity_MW - dispatched_MW
                    # print(g, cap_factor, total_nameplate_capacity_MW, total_instantaneous_capacity_MW, total_stored_capacity_MW, total_available_capacity_MW, dispatched_MW, spare_capacity_MW)
                    regional_timeseries[dt][region]['total_available_capacity_MW'] += total_available_capacity_MW
                    # regional_timeseries[dt][region]['spare_capacity_MW'] += spare_capacity_MW
                    # regional_timeseries[dt][region]['dispatched_MW'] += dispatched_MW
                    classification = labelling.get_tech_classification(g)
                    regional_timeseries[dt][region][classification+'_available_MW'] += total_available_capacity_MW
                
            # Calculate the total available capacity of storage
            if 'stor_level' in timeseries_dict[dt][zone]:
                for g in timeseries_dict[dt][zone]['stor_level']:
                    nameplate_capacity_MW = stor_cap_lookup[zone][g]
                    total_stored_capacity_MW = timeseries_dict[dt][zone]['stor_level'][g] / TIME_PERIOD_HRS
                    total_available_capacity_MW = min(nameplate_capacity_MW, total_stored_capacity_MW)
                    dispatched_MWh = timeseries_dict[dt][zone]['stor_disp'][g]
                    dispatched_MW = dispatched_MWh / TIME_PERIOD_HRS
                    spare_capacity_MW = total_available_capacity_MW - dispatched_MW
                    # print(g, nameplate_capacity_MW, total_stored_capacity_MW, total_available_capacity_MW, dispatched_MW, spare_capacity_MW)
                    regional_timeseries[dt][region]['total_available_capacity_MW'] += total_available_capacity_MW
                    # regional_timeseries[dt][region]['spare_capacity_MW'] += spare_capacity_MW
                    # regional_timeseries[dt][region]['dispatched_MW'] += dispatched_MW
                    classification = labelling.get_tech_classification(g)
                    regional_timeseries[dt][region][classification+'_available_MW'] += total_available_capacity_MW
    return regional_timeseries