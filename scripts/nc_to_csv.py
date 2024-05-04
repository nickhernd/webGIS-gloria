import xarray as xr
from config_python import ConfigPath

data_path = ConfigPath.data_path()

file_nc = data_path + "copernicus_data.nc"
file_cvs = data_path + "copernicus_data.csv"

ds = xr.open_dataset(file_nc)
ds.to_dataframe().to_csv(file_cvs)
