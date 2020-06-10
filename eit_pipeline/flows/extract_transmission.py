from prefect import Parameter, Flow, config
from eit_pipeline.tasks.filesystem import join_path, get_home_path
from eit_pipeline.tasks.io import read_raw_data, save_dataarray
from eit_pipeline.tasks.absorption_imaging import calc_transmission
from eit_pipeline.utils import load_params_for_flow


with Flow('Old2NewDataStructure') as flow:
    local_root = config.data_local['analysis_root']
    seq_path = Parameter('seq_path')
    filename = Parameter('transmission_filename')
    mask_kwargs = Parameter('mask_kwargs')
    polygon_mask_vertices = Parameter('polygon_mask_vertices')

    home_path = get_home_path()
    analysis_path = join_path((home_path, local_root, seq_path))
    out_path = join_path((analysis_path, filename))

    data = read_raw_data(analysis_path)
    trans = calc_transmission(data, mask_kwargs, polygon_mask_vertices)
    save_dataarray(trans, out_path)
    #flow.run_agent()

if __name__ == "__main__":
    params = load_params_for_flow(flow, "../../config-files/old2new.yaml")
    #flow.register(project_name='absorption imaging')
    flow.run(parameters=params)
