# OpenCEM Competition Model
This package takes output from the open capacity expansion model [OpenCEM](http://www.opencem.org.au/) and provides insights into the competitive nature of simulated generation mixes, based on the Network-Extended Residual Supply Index [NERSI](https://github.com/luke-marshall/nersi) measure of electricity market competition.

## Installation

This package uses the poetry package manager. Install poetry with instructions here. Then run `poetry install` to install your dependencies, 

## Maximum Generator Sizing
This script takes the json output files from OpenCEM and generates a timeseries with a number of extracted values (ie.hourly demand, generation for each generator type), as well as the maximum allowable generator size to attain a NERSI > 1 (ie. the maximum size a generator can be without having market power under this measure of pivotality). See maz_generator_size_all_years.sh for further usage hints.

Usage: `poetry run python max_generator_size.py <OPENCEM_JSON_PATH> <OUTPUT_CSV_PATH>`

## Unit Tests
This package uses pytest. You can run the peak price estimator unit tests with `poetry run pytest`