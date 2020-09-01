"""
This script takes a generator size and the 'output' from run.py, 
including the NERSI-based max generator size value for each hour of prospective dispatch, 
and provides an estimate of how many hours would prospectively be peak-priced, if the max 
generator was at that level. 
"""
import sys
import csv
from prettytable import PrettyTable

STATES = ['NSW', 'QLD', 'SA', 'VIC', 'TAS']
BASE_CASE_CEILING_PRICE = 14900.0 #14,900/MWh
BEST_CASE_2SM_CEILING = 500.0

def process(gen_threshold_MW, file_path):
    volumes = {state:0 for state in STATES}
    time_periods = {state:0 for state in STATES}

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for line in reader:
            for state in STATES:
                nersi_max_cap = float(line[state+' nersi_max_capacity'])
                # Condition here is if the largest permissible generator size to prevent market power is less than the threshold being investigated. 
                if nersi_max_cap <= gen_threshold_MW:
                    volumes[state] += float(line[state+' total_demand_MW'])
                    time_periods[state] += 1
    

    # Calculate and print results
    x = PrettyTable()
    x.field_names = ["State", "Number of Pivotal Periods", "Total MWh Demand under Pivotal", "Worst-Case Cost", "Best-Case Cost"]
    for state in STATES:
        peak_price_cost = float(volumes[state]) * BASE_CASE_CEILING_PRICE
        best_case_cost = float(volumes[state]) * BEST_CASE_2SM_CEILING
        x.add_row([state,  f"{round(time_periods[state]):,}", f"{round(volumes[state]):,}", f"${round(peak_price_cost):,}",f"${round(best_case_cost):,}",])
        # print(state,  f"{round(time_periods[state]):,}", f"{round(volumes[state]):,}", f"${round(peak_price_cost):,}",f"${round(best_case_cost):,}",)
    print(x)
                

if __name__ =="__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print("Usage: python peak_price_estimator.py <gen_size> <output_file_path>")
    else:
        gen_threshold_MW = float(sys.argv[1])
        file_path = sys.argv[2]
        print("Calculating for a",gen_threshold_MW,"MW system, for csv file",file_path)
        process(gen_threshold_MW, file_path)
        
