from prefect import Parameter, Flow, config
from eit_pipeline.tasks.filesystem import join_path, get_home_path
from eit_pipeline.tasks.io import read_raw_data, save_dataarray, load_dataarray
from eit_pipeline.tasks.absorption_imaging import calc_transmission
from eit_pipeline.utils import load_params_for_flow

with Flow('calc_peak_od') as flow:
    seq_path = Parameter('seq_path')
    home_path = get_home_path()
    analysis_path = join_path((home_path, config.data_local['analysis_root'], seq_path))
    transmission = load_dataarray(analysis_path/'transmission.h5')

if __name__ == "__main__":
    params = load_params_for_flow(flow, "../../config-files/old2new.yaml")