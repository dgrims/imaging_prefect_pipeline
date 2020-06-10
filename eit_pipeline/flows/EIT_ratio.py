from prefect import Parameter, Flow, config
from eit_pipeline.tasks.filesystem import join_path, get_home_path
from eit_pipeline.tasks.io import read_raw_data, save_dataarray, load_dataarray
from eit_pipeline.tasks.absorption_imaging import calc_transmission, average_od_from_transmission, fit_EIT_dip
from eit_pipeline.tasks.exp_sequence import variables_from_data_array, create_multiindex
from eit_pipeline.utils import load_params_for_flow

with Flow('calc_EIT_ratio') as flow:
    seq_path = Parameter('seq_path')
    home_path = get_home_path()
    analysis_path = join_path((home_path, config.data_local['analysis_root'], seq_path))
    transmission = load_dataarray(analysis_path/'transmission.h5')

    transmission2 = create_multiindex(transmission)
    var = variables_from_data_array(transmission)
    od = average_od_from_transmission(transmission2, var)
    save_dataarray(od, analysis_path/"od.h5")
    #fit_EIT_dip(od, var)


if __name__ == "__main__":
    params = load_params_for_flow(flow, "../../config-files/old2new.yaml")
    flow.run(params)