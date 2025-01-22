# import json
import copernicusmarine as cm
from config_python import ConfigPath
from datetime import datetime, timedelta, date

keys_path = ConfigPath.keys_path()
data_path = ConfigPath.data_path()

# with open("./keys/cmems_credentials.json", "r") as f:
#     credentials = json.load(f)

# cm.login(credentials["username"], credentials["password"])
current_time = date.today()
start_time = current_time.strftime("%Y-%m-%dT00:00:00")
week = timedelta(weeks=1)
current_time = current_time + week
end_time = current_time.strftime("%Y-%m-%dT00:00:00")

print(start_time, end_time)

cm.subset(
    dataset_id="cmems_mod_med_wav_anfc_4.2km_PT1H-i",
    dataset_version="202311",
    variables=["VHM0_WW", "VMDR"],
    minimum_longitude=-1.2928767320590209,
    maximum_longitude=0.8337098052527727,
    minimum_latitude=36.67890882485372,
    maximum_latitude=40.65709226103182,
    start_datetime=start_time,
    end_datetime=end_time,
    output_filename=data_path + "copernicus_data.nc",
    force_download=True,
)


# cm.subset(
#     dataset_id="cmems_mod_med_bgc-bio_anfc_4.2km_P1D-m",
#     dataset_version="202211",
#     variables=["nppv", "o2"],
#     minimum_longitude=-1.2928767320590209,
#     maximum_longitude=0.8337098052527727,
#     minimum_latitude=36.67890882485372,
#     maximum_latitude=40.65709226103182,
#     start_datetime=start_time,
#     end_datetime=end_time,
#     minimum_depth=1,
#     maximum_depth=25,
#     output_filename=data_path + "copernicus_data_ox.nc",
# )

# cm.subset(
#     dataset_id="cmems_mod_med_phy-tem_anfc_4.2km_P1D-m",
#     dataset_version="202311",
#     variables=["bottomT", "thetao"],
#     minimum_longitude=-1.2928767320590209,
#     maximum_longitude=0.8337098052527727,
#     minimum_latitude=36.67890882485372,
#     maximum_latitude=40.65709226103182,
#     minimum_depth=1,
#     maximum_depth=25,
#     output_filename=data_path + "copernicus_data_t.nc",
# )
