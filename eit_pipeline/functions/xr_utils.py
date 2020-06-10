import xarray as xr

def remove_multiindex(da: xr.DataArray, indices):
    try:
        iterator = iter(indices)
    except TypeError:
        da = da.reset_index(indices)
    else:
        for ix in indices:
            da = da.reset_index(ix)
    return da
