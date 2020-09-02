"""
This script takes a generator size and the 'output' from run.py, 
including the NERSI-based max generator size value for each hour of prospective dispatch, 
and provides an estimate of how many hours would prospectively be peak-priced, if the max 
generator was at that level. 
"""
import sys
import csv
from prettytable import PrettyTable
import pendulum
from src.tables import TableManager

REGIONS = ['QLD', 'NSW', 'VIC', 'SA']
BASE_CASE_CEILING_PRICE = 14900.0 #14,900/MWh
BEST_CASE_2SM_CEILING = 500.0

# Market price cap.
MPC = 14900 

TIME_PERIOD_HRS = 1

MW_TO_TW = 1e-6
MW_TO_GW = 1e-6


# Cumulative price bands, taken from the 'Step Change' Scenario of the 2019 Input and Assumption Workbook from AEMO
# https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/nem-forecasting-and-planning/scenarios-inputs-assumptions-methodologies-and-guidelines
# https://aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/inputs-assumptions-methodologies/2020/2020-inputs-and-assumptions-workbook.xlsx?la=en
# Arrays of tuples - tuple is (min price, max price, volume)
SUMMER_FLEX_CUMULATIVE_PRICE_BANDS = {
    'QLD':[ (300, 500, 26.43),  (500, 1000, 45.13), (1000, 7500, 50.20), (7500, MPC, 135.93) ,(MPC, MPC, 854.91)],
    'NSW':[ (300, 500, 564.11),  (500, 1000, 1057.55), (1000, 7500, 1084.05), (7500, MPC, 1267.11) ,(MPC, MPC, 1267.11)],
    'VIC':[ (300, 500, 151.09),  (500, 1000, 504.61), (1000, 7500, 542.05), (7500, MPC, 652.85) ,(MPC, MPC, 926.56)],
    'SA':[ (300, 500, 35.86),  (500, 1000, 97.18), (1000, 7500, 108.14), (7500, MPC, 298.78) ,(MPC, MPC, 298.78)],
    'TAS':[ (300, 500, 0.0),  (500, 1000, 1.79), (1000, 7500, 60.59), (7500, MPC, 60.59) ,(MPC, MPC, 60.59)],
}

WINTER_FLEX_CUMULATIVE_PRICE_BANDS = {
    'QLD':[(300, 500, 25.07) , (500,1000, 42.80),  (1000, 7500, 47.62), (7500, MPC, 128.93) ,(MPC, MPC, 730.0)],
    'NSW':[ (300, 500, 444.44), (500, 1000, 833.21), (1000, 7500, 854.09), (7500, MPC, 998.31) ,(MPC, MPC, 998.31)],
    'VIC':[ (300, 500, 180.09),  (500, 1000, 601.46), (1000, 7500, 646.09), (7500, MPC, 778.15) ,(MPC, MPC, 778.15)],
    'SA':[ (300, 500, 26.81),  (500, 1000, 72.65), (1000, 7500, 80.84), (7500, MPC, 223.35) ,(MPC, MPC, 223.35)],
    'TAS':[ (300, 500, 0.0),  (500, 1000, 2.21), (1000, 7500, 75.0), (7500, MPC, 75.0) ,(MPC, MPC, 75.0)],
}

tables = TableManager()

def generate_demand_curve_from_price_bands(price_bands, total_demand):
    """
    Takes a series of ordered cumulative price bands (as in the AEMO assumptions workbook) 
    and a total demand, arranges into a piecewise demand curve.
    """
    demand_curve = []
    
    # Assemble the flex part of the demand curve
    remaining_demand = total_demand
    cumulative_volume = 0
    for band in price_bands:
        value = band[0]
        volume = band[2] - cumulative_volume

        if value == MPC:
            demand_curve.append((value, remaining_demand))
        else:
            demand_curve.append((value, min(volume, remaining_demand)))
        
        cumulative_volume += volume
        remaining_demand = max(remaining_demand - volume, 0)

        if remaining_demand == 0:
            break
    
    # If there's no final MPC band with any remaining demand, add it. 
    if remaining_demand > 0 and demand_curve[-1][0] != MPC:
        demand_curve.append((MPC, remaining_demand))

    # We were ascending in price - we want to make it descending instead.
    demand_curve = list(reversed(demand_curve))
    return demand_curve


def possible_withholding_MW(gen_size, max_gen_size, total_demand):
    """
    Takes the investigated generator size (MW) and the maximum generator size (to stay under NERSI threshold), 
    calculates how many MW could be withheld for profit if the investigated generator has market power.
    """
    return max(min(total_demand, gen_size - max_gen_size), 0)

def closer_to_winter(dt):
    midwinter = pendulum.datetime(dt.year, 7,16)
    # If it's after 10 October or before 4 August in the same year, it's closer to summer. Otherwise closer to winter. 
    if dt > pendulum.datetime(dt.year, 10,16) :
        return False
    elif dt < pendulum.datetime(dt.year, 4, 16):
        return False
    else:
        return True

def get_two_sided_market_demand_curve(dt, total_demand, region):
    """Given a datetime, return the demand curve as piecewise constant monotone decreasing function 
    (array of price-volume tuples).
    """
    # Determine whether to use the AEMO summer or winter price bands. 
    if closer_to_winter(dt):
        price_bands = WINTER_FLEX_CUMULATIVE_PRICE_BANDS[region]
    else:
        price_bands = SUMMER_FLEX_CUMULATIVE_PRICE_BANDS[region]
    # Generate a demand curve from the price bands. 
    return generate_demand_curve_from_price_bands(price_bands, total_demand)

def get_single_sided_market_demand_curve(total_demand):
    return [(MPC, total_demand)]

def make_rational_bid_decision (possible_withholding_MW, demand_curve):
    """
    Given a maximum possible withholding volume and assuming that this is the marginal generator, 
    examine the demand curve and make the most valuable decision for this time period. 
    Returns a price, volume tuple. 
    """
    # Work backwards from the end of the demand curve, assemble all possible rational candidate bids by taking maximum volume shadow bid at each price point. 
    candidate_bids = []
    remaining_volume = 0
    for demand_bid in reversed(demand_curve):
        shadow_price = demand_bid[0] - 1
        # Volume available at a given demand level.
        volume = max(min(demand_bid[1], possible_withholding_MW - remaining_volume), 0)
        candidate_bids.append( (shadow_price, volume))
        remaining_volume += volume

    # Loop through all the candidate bids, see which one earns the most.
    
    candidate = candidate_bids[0]
    for bid in candidate_bids:
        # Bid earns volume dispatched * price. 
        if bid[0] * bid[1] > candidate[0] * candidate[1]:
            candidate = bid
        # If bid has same return but lower volume dispatched, favour lower volume
        elif bid[0] * bid[1] == candidate[0] * candidate[1] and bid[1] < candidate[1]:
            candidate = bid
        
    # Return the bid with the highest return
    return candidate


    
def process(gen_threshold_MW, file_path):
    print("\nCalculating competitive metrics for a",gen_threshold_MW,"MW system, for csv file",file_path,"\n")

    with open(file_path) as f:
        reader = csv.DictReader(f)
        # Slots to record metrics
        count_of_mp_opportunities = {r:0 for r in REGIONS}
        total_savings = {r:0 for r in REGIONS}
        demand_response_volume = {r:0 for r in REGIONS}
        cumulative_demand_volume = {r:0 for r in REGIONS}
        total_2sm_energy_cost = {r:0 for r in REGIONS}

        for line in reader:
            dt = pendulum.parse(line['Date '])
     
            for region in REGIONS:
                
                total_demand = float(line[region+' total_demand_MW'])
                nersi_max_cap_MW = float(line[region+' nersi_max_capacity'])
                
                # Calculate the maximum volume it is possible for the generator to withhold. 
                max_withholding_volume  = possible_withholding_MW(gen_threshold_MW, nersi_max_cap_MW, total_demand)
                # if it is possible for the generator to withhold some volume in this time period, calculate the rational decision for flexible and inflexible demand curves. 
                if max_withholding_volume > 0:
                    # Make a two-sided market decision.
                    demand_curve_2sm = get_two_sided_market_demand_curve(dt, total_demand, region)
                    decision_2sm = make_rational_bid_decision(max_withholding_volume, demand_curve_2sm)

                    # Make a single-sided market decision.
                    demand_curve_1sm = get_single_sided_market_demand_curve(total_demand)
                    decision_1sm = make_rational_bid_decision(max_withholding_volume, demand_curve_1sm)

                    # Calculate the magnitude of the demand response in relation to the 2sm decision. 
                    demand_response_MW = max_withholding_volume - decision_2sm[1]

                    # Record relevant metrics
                    count_of_mp_opportunities[region] += 1
                    total_savings[region] += (decision_1sm[0] * total_demand) - (decision_2sm[0] * (total_demand - demand_response_MW))
                    demand_response_volume[region] += demand_response_MW
                    cumulative_demand_volume[region] += total_demand
                    total_2sm_energy_cost[region] += (total_demand - demand_response_MW) * decision_2sm[0]

                    # print(region, dt, total_demand, nersi_max_cap_MW, max_withholding_volume, decision_1sm, decision_2sm)
        
        
        # Record relevant metrics to table for printing and analysis.
        tables.add_row('Count of Market Power Opportunities', [gen_threshold_MW]+[count_of_mp_opportunities[r] for r in REGIONS])
        tables.add_row('Total $ Savings', [gen_threshold_MW]+[total_savings[r] for r in REGIONS])
        tables.add_row('Average 2SM Market Price During MP Events', [gen_threshold_MW]+[total_2sm_energy_cost[r] / (cumulative_demand_volume[r] - demand_response_volume[r]) if cumulative_demand_volume[r] > 0 else 0 for r in REGIONS])
        tables.add_row('Total Original Demand During MP Events', [gen_threshold_MW]+[cumulative_demand_volume[r] * TIME_PERIOD_HRS * MW_TO_GW for r in REGIONS])
        tables.add_row('Total DR Volume (GWh) During MP Events', [gen_threshold_MW]+[demand_response_volume[r] * TIME_PERIOD_HRS * MW_TO_GW for r in REGIONS])
        tables.add_row('DR as Percent of Total Demand During MP Events', [gen_threshold_MW]+[100.0 * demand_response_volume[r] / cumulative_demand_volume[r]  if cumulative_demand_volume[r] > 0 else 0 for r in REGIONS])
        
        


def process_old(gen_threshold_MW, file_path):
    volumes = {state:0 for state in REGIONS}
    time_periods = {state:0 for state in REGIONS}

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for line in reader:
            for state in REGIONS:
                nersi_max_cap = float(line[state+' nersi_max_capacity'])
                # Condition here is if the largest permissible generator size to prevent market power is less than the threshold being investigated. 
                if nersi_max_cap <= gen_threshold_MW:
                    volumes[state] += float(line[state+' total_demand_MW'])
                    time_periods[state] += 1

    # Calculate and print results
    x = PrettyTable()
    x.field_names = ["State", "Number of Pivotal Periods", "Total MWh Demand under Pivotal", "Worst-Case Cost", "Best-Case Cost"]
    for state in REGIONS:
        peak_price_cost = float(volumes[state]) * BASE_CASE_CEILING_PRICE
        best_case_cost = float(volumes[state]) * BEST_CASE_2SM_CEILING
        x.add_row([state,  f"{round(time_periods[state]):,}", f"{round(volumes[state]):,}", f"${round(peak_price_cost):,}",f"${round(best_case_cost):,}",])
        # print(state,  f"{round(time_periods[state]):,}", f"{round(volumes[state]):,}", f"${round(peak_price_cost):,}",f"${round(best_case_cost):,}",)
    print(x)



if __name__ =="__main__":
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Not enough arguments. Usage: python peak_price_estimator.py <input_file_path>")
    else:
        
        file_path = sys.argv[1]

        tables.set_field_names('Count of Market Power Opportunities',['Generator Size']+[r for r in REGIONS])
        tables.set_field_names('Total $ Savings',['Generator Size']+[r for r in REGIONS])
        tables.set_field_names('Average 2SM Market Price During MP Events',['Generator Size']+[r for r in REGIONS])
        tables.set_field_names('Total Original Demand During MP Events',['Generator Size']+[r for r in REGIONS])
        tables.set_field_names('Total DR Volume (GWh) During MP Events',['Generator Size']+[r for r in REGIONS])
        tables.set_field_names('DR as Percent of Total Demand During MP Events',['Generator Size']+[r for r in REGIONS])
        
        process(200, file_path)
        process(500, file_path)
        process(1000, file_path)
        process(2000, file_path)
        process(5000, file_path)
        process(10000, file_path)
        
        tables.print_tables()
        tables.export_tables_to_csv('two_sided_market_results.csv')





    

