from nersi.market import NodalMarket
from nersi.calculator import calculate_max_generator_capacity



def setup_market(intercon_cap_lookup):
    print(intercon_cap_lookup)
    market = NodalMarket()
    market.add_node('NSW')
    market.add_node('VIC')
    market.add_node('SA')
    market.add_node('QLD')
    market.add_node('TAS')

    # Terranora is SEQ <> NNS
    market.set_transmission('NSW', 'QLD', intercon_cap_lookup['NNS']['SEQ'], "Terranora NSW->QLD")
    market.set_transmission('QLD', 'NSW', intercon_cap_lookup['SEQ']['NNS'], "Terranora QLD->NSW")

    # QNI is SWQ <> NNS
    market.set_transmission('NSW', 'QLD', intercon_cap_lookup['NNS']['SWQ'], "Queensland NSW Interconnector (QNI) NSW->QLD")
    market.set_transmission('QLD', 'NSW', intercon_cap_lookup['SWQ']['NNS'], "Queensland NSW Interconnector (QNI) QLD->NSW")

    # Victoria to NSW Interconnector
    market.set_transmission('VIC', 'NSW', intercon_cap_lookup['NVIC']['SWNSW'], "Victoria to NSW Interconnector VIC->NSW")
    market.set_transmission('NSW', 'VIC', intercon_cap_lookup['SWNSW']['NVIC'], "Victoria to NSW Interconnector NSW->VIC")

    # Additional physical connection NSW to CVIC. 
    market.set_transmission('VIC', 'NSW', intercon_cap_lookup['CVIC']['SWNSW'], "Physical Connection CVIC and NSW VIC->NSW")
    market.set_transmission('NSW', 'VIC', intercon_cap_lookup['SWNSW']['CVIC'], "Physical Connection CVIC and NSW NSW->VIC")

    # Basslink
    market.set_transmission('TAS', 'VIC', intercon_cap_lookup['TAS']['LV'], "Basslink TAS->VIC")
    market.set_transmission('VIC', 'TAS', intercon_cap_lookup['LV']['TAS'], "Basslink VIC->TAS")
    
    # Heywood
    market.set_transmission('VIC', 'SA', intercon_cap_lookup['MEL']['SESA'], "Heywood Interconnector VIC->SA")
    market.set_transmission('SA', 'VIC', intercon_cap_lookup['SESA']['MEL'], "Heywood Interconnector SA->VIC")

    # Murraylink
    market.set_transmission('VIC', 'SA', intercon_cap_lookup['CVIC']['NSA'], "Murraylink VIC->SA")
    market.set_transmission('SA', 'VIC', intercon_cap_lookup['NSA']['CVIC'], "Murraylink SA->VIC")

    # # New Transmission NSW to SA
    market.set_transmission('NSW', 'SA', intercon_cap_lookup['SWNSW']['NSA'], "New Transmission NSW to SA")
    market.set_transmission('SA', 'NSW', intercon_cap_lookup['NSA']['SWNSW'], "New Transmission NSW to SA")

    # # New Transmission Vic - Tas
    market.set_transmission('VIC', 'TAS', intercon_cap_lookup['MEL']['TAS'], "New Transmission Vic to Tas")
    market.set_transmission('TAS', 'VIC', intercon_cap_lookup['TAS']['MEL'], "New Transmission Vic to Tas")

    return market


def apply_nersi(timeseries, intercon_cap_lookup):
    market = setup_market(intercon_cap_lookup)
    # market.draw()
    market.print()
    for dt in timeseries:
        print("NERSI:",dt)
        # Calculate and add all available surplus capacity to nodes. 
        for region in timeseries[dt]:
            # print("\n",region)
            # print (timeseries[dt])
            # Surplus is either zero or positive for NERSI calc. Excess demand gets modelled as zero. 
            surplus = max(timeseries[dt][region]['total_available_capacity_MW'] - timeseries[dt][region]['total_demand_MW'], 0)
            market.set_surplus_capacity(region, surplus)
        
        # Calculate NERSI for each 
        for region in timeseries[dt]:
            region_demand = timeseries[dt][region]['total_demand_MW']
            region_available_capacity = timeseries[dt][region]['total_available_capacity_MW']
            max_capacity = calculate_max_generator_capacity(market, region, region_demand, region_available_capacity)
            # print(region, max_capacity)
            timeseries[dt][region]['nersi_max_capacity'] = max_capacity

        market.clear_surplus_capacity()
    return timeseries
    
