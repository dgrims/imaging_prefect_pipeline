from rydanalysis import AbsorptionImaging, OldStructure, ExpSequence, ReferenceAnalysis, RectangularMask, EllipticalMask
from prefect import task

@task
def variables_from_data_array(da):
    coords = da.coords
    dims = coords.dims
    variables = {variable: coords[variable] for variable in coords if variable not in dims}
    return list(variables.keys())[0]

@task
def create_multiindex(ds):
        coord_keys = [coord for coord in ds.coords.keys() if coord not in {'x', 'y', 'time'}]
        #coord_keys.remove('x')
        #coord_keys.remove('y')
        #coord_keys.remove('time')
        ds = ds.set_index(shot=coord_keys)
        return ds