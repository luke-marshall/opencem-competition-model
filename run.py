import sys
import json
from src.competition_model import apply_nersi
import os
import src.output as output
import src.processing as processor







if __name__ == "__main__":
    
    timeseries_dict = {}
    

    if len(sys.argv) < 3:
        print("Please provide the filename / path of an OpenCEM json output file, and the desired output folder.")
    else:
        filepath = sys.argv[1]
        output_dir = sys.argv[2]
        # Create the output directory before you start. 
        if not os.path.exists(output_dir):
            print("Creating Output File Directory")
            os.makedirs(output_dir)
        
        print("Processing raw data from OpenCEM")
        with open(filepath) as f:
            data = json.load(f)
            for year in data:
                print(data[year]['sets']['regions'])
                print(data[year]['sets']['zones_in_regions'])
                
                region_net_demand = data[year]['params']['region_net_demand']
                gen_cap_factor = data[year]['params']['gen_cap_factor']
                hyb_cap_factor = data[year]['params']['hyb_cap_factor']
                
                unserved = data[year]['vars']['unserved']
                surplus = data[year]['vars']['surplus']
                
                gen_cap_op = data[year]['vars']['gen_cap_op']
                hyb_cap_op = data[year]['vars']['hyb_cap_op']
                stor_cap_op = data[year]['vars']['stor_cap_op']
                
                gen_disp = data[year]['vars']['gen_disp']
                stor_disp = data[year]['vars']['stor_disp']
                hyb_disp = data[year]['vars']['hyb_disp']

                stor_level = data[year]['vars']['stor_level']
                # stor_charge = data[year]['vars']['stor_charge']
                hyb_level = data[year]['vars']['hyb_level']
                hyb_charge = data[year]['vars']['hyb_charge']

                intercon_cap_op = data[year]['vars']['intercon_cap_op']

                timeseries_dict = processor.process_unserved(unserved, timeseries_dict)
                timeseries_dict = processor.process_surplus(unserved, timeseries_dict)
                
                timeseries_dict = processor.process_gen_cap_factor(gen_cap_factor, timeseries_dict)
                timeseries_dict = processor.process_hyb_cap_factor(hyb_cap_factor, timeseries_dict)

                timeseries_dict = processor.process_gen_disp(gen_disp, timeseries_dict)
                timeseries_dict = processor.process_stor_disp(stor_disp, timeseries_dict)
                timeseries_dict = processor.process_hyb_disp(hyb_disp, timeseries_dict)

                timeseries_dict = processor.process_stor_level(stor_level, timeseries_dict)
                # timeseries_dict = processor.process_stor_charge(stor_charge, timeseries_dict)
                timeseries_dict = processor.process_hyb_level(hyb_level, timeseries_dict)
                timeseries_dict = processor.process_hyb_charge(hyb_charge, timeseries_dict)
                
                gen_cap_lookup = processor.process_cap_op(gen_cap_op)
                hyb_cap_lookup = processor.process_cap_op(hyb_cap_op)
                stor_cap_lookup = processor.process_cap_op(stor_cap_op)
                intercon_cap_lookup = processor.process_intercon_cap_op(intercon_cap_op)

                regional_demand_timeseries = processor.process_region_net_demand(region_net_demand)

    print("Finished loading data.")
    print("Creating Regional timeseries from zone data.")
    regional_timeseries = processor.process_zonal_timeseries(timeseries_dict, gen_cap_lookup, hyb_cap_lookup, stor_cap_lookup, regional_demand_timeseries)
    print("Applying NERSI")
    regional_timeseries = apply_nersi(regional_timeseries, intercon_cap_lookup)

    print("Writing to Output File")
    file_name = os.path.split(filepath)[-1]
    file_name = os.path.splitext(file_name)[0]
    
    output.regional_timeseries_to_csv(regional_timeseries, file_name+'.csv', output_dir)
    print("Finished. Output written to ", os.path.join(output_dir, file_name+'.csv'))
