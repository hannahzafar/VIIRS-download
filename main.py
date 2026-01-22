#!/usr/bin/env python

import earthaccess
import xarray as xr

from query_functions import download_results, query_files

results, folder_name = query_files()
# print(results[0], len(results))

# download_results(results, folder_name)

results = results[0]
# results = [results[0]]
print(results)
print("\n")
print(earthaccess.open(results))
print("\n")
print(earthaccess.open(results)[0])
print("\n")
# fileobjects = earthaccess.open(results)
ds = xr.open_dataset(
    # fileobjects[0],
    earthaccess.open(results)[0],
    engine="h5netcdf",
    group="/HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data Fields",
)

# ds = xr.open_mfdataset(
#     earthaccess.open(results),
#     group="/HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data Fields",
#     engine="h5netcdf",
#     combine="nested",
#     compat="override",
# )

print(ds)
