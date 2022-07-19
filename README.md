# Experiments with Kerchunk

This repo contains some (hopefully working) example code for demonstrating the use of [Kerchunk](https://fsspec.github.io/kerchunk/).

The basic idea is to store [NetCDF4](https://www.unidata.ucar.edu/software/netcdf/) data on a remote HTTP(S) server that supports range requests. Kerchunk makes the NetCDF4 data look like a [Zarr](https://zarr.readthedocs.io/) dataset through the creation of an index file. Using this index, client code can read data directly into xarray over HTTP(S). Only the data chunks that are needed are read.

Code in this repo demonstrates:
1. Setting up a working Python environment
2. Creating a Zarr index file
3. Reading data into xarray over HTTP(S)
4. Using an HTTP(S) proxy (e.g. [HTTP Toolkit](https://httptoolkit.tech/python/))

In future work I'll expand this to indexing several NetCDF4 files. Note that this code does not require specific use of [Amazon S3](https://aws.amazon.com/s3/) or compatible protocols; everything is done over plain HTTP(S).

## 1. Environment setup

I'm on an M1 Mac, which gave me a few [headaches](https://github.com/fsspec/kerchunk/issues/195) in getting all the dependencies installed. I found it necessary to install most dependencies via [conda-forge](https://conda-forge.org), in order to get a version of the [numcodecs](https://numcodecs.readthedocs.io/) libary that enables decoding of NetCDF4 files.

The provided `environment.yml` file defines the conda and pip dependencies and can be used to create an environment as follows:
```
conda create --file environment.yml
conda activate kerchunk-test
```

Or, for a more manual setup:
```
conda create --name kerchunk-test
conda activate kerchunk-test
conda config --env --add channels conda-forge 
conda config --env --set channel_priority strict
conda install python=3.10 h5py zarr requests aiohttp fsspec xarray matplotlib jinja2
pip install kerchunk
```
Through this latter configuration, conda-forge is set as the default package location _for this environment only_.


Note that althought there is only one environment defined in this repo, the processes of creating the index and reading the file have different dependencies. For example, when reading the file, we need `xarray` and `matplotlib` (which we don't need when creating the index), but we don't need `h5py` or `kerchunk` itself.

## 2. Creating a Zarr index file
The process of creating the index file can take a very long time, even for a single NetCDF4 file, if it is done over a remote connection (depending on the NetCDF4 file, there can be hundreds of individual reads over the network). For that reason, I recommend you download the file to a local machine for your experiments, editing `create_index.py` as appropriate.

```
python create_index.py > index.json
```

## 3. Reading remote NetCDF4 data
The script `plot_data.py` demonstrates reading and plotting data from a NetCDF4 file that has been previously indexed. Note that the index file can be on your local system, while the NetCDF4 file can be remote.

```
python plot_data.py
```

If you have indexed a different NetCDF4 file, you will have to edit this script to select the right variables and coordinates.


## 4. Using an HTTP(S) proxy
If you would like to look at what is going on between the client and the server (during indexing or reading the data), you can use an HTTP(S) proxy. I used [HTTP Toolkit](https://httptoolkit.tech/python/).

Note that, although HTTP Toolkit provides a bash script for setting the right environment variables, I found that these environment variables are ignored by the above scripts. You will need to include the proxy server URL in the relevant parts of the code. You will probably also have to tell the system to ignore SSL certificate checks (see code examples), otherwise the code may complain about the proxy server's self-signed certificates.

For example:
```python
with fsspec.open(URL, "rb", proxy="http://127.0.0.1:8000", ssl=False) as f:
    h5chunks = kerchunk.hdf.SingleHdf5ToZarr(f, URL, inline_threshold=100)
    print(json.dumps(h5chunks.translate()))
```
`http://127.0.0.1:8000` is the default URL for the HTTP Toolkit proxy server.

I believe that the actual HTTP(S) communication is being done through [aiohttp](https://docs.aiohttp.org/). Options connected with HTTP(S) connections are passed to this underlying library.

