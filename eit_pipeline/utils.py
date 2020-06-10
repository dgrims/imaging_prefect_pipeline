from ruamel import yaml


def load_params_for_flow(flow, path):
    with open(path, 'r') as param_file:
        parameters = yaml.load(param_file, Loader=yaml.Loader)
    parameters = {p.name: parameters[p.name] for p in flow.parameters()}
    return parameters