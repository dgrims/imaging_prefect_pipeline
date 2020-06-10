from prefect import Flow, Parameter
from eit_pipeline.tasks.io import seq_from_old_structure, save_raw_data
from eit_pipeline.tasks.filesystem import join_path, safe_create_dir, get_home_path
from eit_pipeline.utils import load_params_for_flow
from prefect import context

with Flow('Old2NewDataStructure') as flow:
    local_root = Parameter('local_root')
    data_root = Parameter('data_root')
    seq_path = Parameter('seq_path')
    home_path = get_home_path()


    data_path = join_path((home_path, data_root, seq_path))
    analysis_path = join_path((home_path, local_root, seq_path))
    analysis_path_2 = safe_create_dir(analysis_path)

    seq = seq_from_old_structure(data_path)
    save_raw_data(seq, analysis_path_2)

if __name__ == "__main__":
    params = load_params_for_flow(flow, "../../config-files/old2new.yaml")
    flow.register(project_name='absorption imaging')
    #flow.run(parameters=params)
