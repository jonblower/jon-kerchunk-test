# Example of creating a Zarr index file from a NetCDF file
# using kerchunk

import json
import fsspec
import kerchunk.hdf

FILENAME = "1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc"
URL = "https://cmip6-zarr-o.s3-ext.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/" + FILENAME

# Here we assume we have downloded the file locally, otherwise
# the process of creating the index can be very long. However, the index file
# itself will still point to the full remote URL.
#
# If you want to create the index file directly from the URL, simply 
# replace FILENAME with URL in the open() command.
#
# If you want to use an HTTP(S) proxy server like HTTP Toolkit,
# open the file like this:
#with fsspec.open(URL, proxy="http://127.0.0.1:8000", ssl=False) as f:

with fsspec.open(FILENAME) as f:
    h5chunks = kerchunk.hdf.SingleHdf5ToZarr(f, URL, inline_threshold=100)
    print(json.dumps(h5chunks.translate()))