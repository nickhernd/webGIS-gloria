import xarray as xr
from config_python import ConfigPath

data_path = ConfigPath.data_path()

file_nc = [
    data_path + "copernicus_data.nc",
    # data_path + "copernicus_data_t.nc",
    # data_path + "copernicus_data_ox.nc",
]

file_csv = [
    data_path + "copernicus_data.csv",
    # data_path + "copernicus_data_t.csv",
    # data_path + "copernicus_data_ox.csv",
]

for file_in, file_out in zip(file_nc, file_csv):
    ds = xr.open_dataset(file_in)
    ds.to_dataframe().to_csv(file_out)
