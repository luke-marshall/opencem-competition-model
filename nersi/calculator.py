
def calculate_max_generator_capacity_old_working(market, region, region_demand, region_available_capacity):
    """
        Calculates the maximum generator capacity in a region, for all generators in that region to have a NERSI greater than 1. 
    """
    STEP_SIZE = 20
    if region_demand <= STEP_SIZE * 2:
        return region_available_capacity
    

    for generator_capacity in reversed(range(0,int(region_demand+STEP_SIZE),STEP_SIZE )):
        nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
        if nersi >= 1:
            # print("nersi",nersi)
            break
    
    # if generator_capacity >= region_demand:
    #     return None
    # else:
    return generator_capacity


def calculate_max_generator_capacity_slow(market, region, region_demand, region_available_capacity):
    """
        Calculates the maximum generator capacity in a region, for all generators in that region to have a NERSI greater than 1. 
    """
    STEP_SIZE = 100
    NERSI_THRESHOLD = 1
    if region_demand <= STEP_SIZE:
        return region_available_capacity
    
    generator_capacity = 0
    nersi = NERSI_THRESHOLD + 1
    while nersi > NERSI_THRESHOLD:
        nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
        # print(generator_capacity,nersi)
        generator_capacity += STEP_SIZE

    # for generator_capacity in reversed(range(0,int(region_demand+STEP_SIZE),STEP_SIZE )):
    #     nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
    #     if nersi >= 1:
    #         # print("nersi",nersi)
    #         break
    
    # if generator_capacity >= region_demand:
    #     return None
    # else:
    return generator_capacity

def average(val_1, val_2):
    return ( float(val_1) + float(val_2) ) / 2

def calculate_max_generator_capacity(market, region, region_demand, region_available_capacity):
    """
        Calculates the maximum generator capacity in a region, for all generators in that region to have a NERSI greater than 1. 
    """
    STEP_SIZE = 20
    NERSI_THRESHOLD = 1
    if region_demand <= STEP_SIZE:
        return region_available_capacity
    
    # generator_capacity = 0
    # nersi = NERSI_THRESHOLD + 1
    # while nersi > NERSI_THRESHOLD:
    #     nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
    #     # print(generator_capacity,nersi)
    #     generator_capacity += STEP_SIZE


    low_bound = 0
    high_bound = region_demand * 3
    generator_capacity = average(high_bound, low_bound)

    while(high_bound - low_bound > STEP_SIZE):
        nersi = calculate_nersi(market, region, region_demand,region_available_capacity, generator_capacity)
        # If greater than the NERSI threshold, generator_cap is too small (ie there is sufficient competition.)
        # So set lower bound to the gen_cap
        if nersi > NERSI_THRESHOLD:
            low_bound = generator_capacity
        else:
            high_bound = generator_capacity

        generator_capacity = average(high_bound, low_bound)

    return generator_capacity


def calculate_nersi(market, region, region_demand, region_available_capacity, generator_capacity):
    """
        Given a market model with transmission constraints and surplus capacities set, 
        calculates the Network-Extended Residual Supply Index for a market participant (with capacity <generator_capacity>) 
        in a given region, with a set demand (in the same units as gen capacity) and available capacity from all generators (including the generator under investigation)
    """
    max_flow = market.calculate_max_flow(region)
    total_available = max_flow + region_available_capacity - generator_capacity
    nersi = max(total_available,0) / region_demand
    return nersi



