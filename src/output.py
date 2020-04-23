import os

def regional_timeseries_to_csv(regional_timeseries, filename, output_dir):
    header_written = False

    with open(os.path.join(output_dir,filename), 'w+') as output_file:
        
        # Write the header
        header_string = "Date ,"
        for dt in sorted([t for t in regional_timeseries]):
            for region in sorted([r for r in regional_timeseries[dt]]):
                for data_type in sorted([d for d in regional_timeseries[dt][region]]):
                    header_string += region+" "+data_type+","
            break
        output_file.write(header_string+'\n')
        # Write each row
        
        for dt in sorted([t for t in regional_timeseries]):
            row_string = str(dt)+","
            for region in sorted([r for r in regional_timeseries[dt]]):
                for data_type in sorted([d for d in regional_timeseries[dt][region]]):
                    row_string+= str(regional_timeseries[dt][region][data_type])+","
            output_file.write(row_string+'\n')
            