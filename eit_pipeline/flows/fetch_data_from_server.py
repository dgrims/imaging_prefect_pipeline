import prefect
from prefect import Parameter
from eit_pipeline.tasks.io import seq_from_old_structure, save_raw_data
from eit_pipeline.tasks.filesystem import join_path, safe_create_dir, get_home_path
from eit_pipeline.tasks.server import fetch_remote_data
from eit_pipeline.utils import load_params_for_flow


with prefect.Flow('fetch_data_from_server') as flow:
    conf = prefect.config
    seq_path = Parameter('seq_path')
    home_path = get_home_path()

    password = prefect.context.secrets['data_server_password']

    remote_data_path = join_path((conf.data_server['root'], seq_path))
    analysis_path = join_path((home_path,  conf.data_local['analysis_root'], seq_path))
    local_data_path = join_path((home_path,  conf.data_local['data_root'], seq_path))

    data_path = fetch_remote_data(conf.data_server['ip'],
                                  conf.data_server['port'],
                      conf.data_server['user'],
                      password,
                      conf.data_local['hostname'],
                      conf.data_server['remote_name'],
                      conf.data_server['domain'],
                      conf.data_server['share'],
                      remote_data_path,
                      local_data_path)

    analysis_path_2 = safe_create_dir(analysis_path)
    seq = seq_from_old_structure(data_path)
    save_raw_data(seq, analysis_path_2)
    flow.run_agent()

if __name__ == "__main__":
    params = load_params_for_flow(flow, "../../config-files/old2new.yaml")
    flow.register(project_name='absorption imaging')

    #flow.run(parameters=params)
