
def calculate_max_generator_capacity(market, region, region_demand, region_available_capacity):
    """
        Calculates the maximum generator capacity in a region, for all generators in that region to have a NERSI greater than 1. 
    """
    
    if region_demand <= 0:
        return region_available_capacity
    
    
    # nersi = 0
    # generator_capacity = 1

    for generator_capacity in reversed(range(0,int(region_available_capacity), 100)):
        nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
        if nersi < 1:
            return generator_capacity
    
    return 1
    
    # while nersi < 1 and generator_capacity < region_available_capacity:
    #     nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
    #     generator_capacity += 10
    #     print(nersi, generator_capacity,)
    
    # return generator_capacity



def calculate_nersi(market, region, region_demand, region_available_capacity, generator_capacity):
    """
        Given a market model with transmission constraints and surplus capacities set, 
        calculates the Network-Extended Residual Supply Index for a market participant (with capacity <generator_capacity>) 
        in a given region, with a set demand (in the same units as gen capacity) and available capacity from all generators (including the generator under investigation)
    """
    max_flow = market.calculate_max_flow(region)
    
    total_available = max_flow + region_available_capacity - generator_capacity
    nersi = max(total_available,0) / region_demand

    # print("Nersi",nersi,"Max flow", max_flow, "av_cap", region_available_capacity, 'gen_cap', generator_capacity)
    return nersi
