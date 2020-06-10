from prefect import task
from rydanalysis import AbsorptionImaging, OldStructure, ExpSequence, ReferenceAnalysis, RectangularMask, EllipticalMask
from pathlib import Path
from eit_pipeline.functions.xr_utils import remove_multiindex
import xarray as xr

@task
def seq_from_old_structure(path):
    assert Path(path).is_dir()
    seq = OldStructure(path)
    return seq

@task
def save_raw_data(seq, path):
    seq.save_raw_data(path=path)

@task
def read_raw_data(path):
    seq = ExpSequence(path)
    return seq.raw_data

@task
def load_dataarray(path):
    return xr.load_dataarray(path)


@task
def save_dataarray(da, path, reset_indice=None):
    path.parents[0].mkdir(parents=True, exist_ok=True)
    try:
        da = remove_multiindex(da, ['shot'])
    except KeyError:
        print('WARNING: could not reset multiindices')
    da.to_netcdf(path)


