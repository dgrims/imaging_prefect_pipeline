from prefect import task
from pathlib import Path


@task
def safe_create_dir(path):
    path = Path(path)
    try:
        path.mkdir(parents=True,)
    except FileExistsError:
        pass
    return path

@task
def join_path(path_list):
    joined = Path()
    for path in path_list:
        joined = joined/path
    return joined

@task
def is_file(path):
    path = Path(path)
    return path.is_file()

@task
def get_home_path():
    return Path.home()

