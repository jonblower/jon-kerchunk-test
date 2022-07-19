# Reads a NetCDF4 dataset that was previously indexed, e.g. by create_index.py
# The index is in a file called index.json

import xarray as xr
import matplotlib.pyplot as plt

# TODO: can this be simplified through use of open_zarr()?
ds = xr.open_dataset(
    "reference://",
    engine="zarr",
    backend_kwargs={
        "decode_times" : False,
        "storage_options": {
            "fo": "index.json",
            "remote_protocol": "https",
            # Uncomment these lines to enable the proxy
            #"remote_options": {
            #    "proxy": "http://127.0.0.1:8000",
            #    "ssl": False
            #}
        },
        "consolidated": False
    }
)

# You can adjust the time and level indices
subset = ds['hus'].isel(time=0, plev=0)
print(subset)

subset.plot()
plt.show()