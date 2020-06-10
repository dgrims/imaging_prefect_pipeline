from smb import SMBConnection
from pathlib import Path
from prefect import task
from datetime import timedelta


def main():
    con = SMBConnection.SMBConnection('grimshandl',
                                      'qdten016',
                                      'BW5-PC-4',
                                      'AXION',
                                      ''
                                      )
    assert con.connect('147.142.18.81')
    print(con.listShares())


def smb_copy_folder(con: SMBConnection, share, remote_path, local_path):
    remote_path = str(remote_path)
    print('Walking path', remote_path)
    path_list = con.listPath(share, remote_path)
    for p in path_list:
        if p.filename != '.' and p.filename != '..':
            parent_path = remote_path
            local_parent_path = local_path
            if not parent_path.endswith('/'):
                parent_path += '/'

            if p.isDirectory:

                (local_parent_path / Path(p.filename)).mkdir(parents=True, exist_ok=True)
                smb_copy_folder(con, share, parent_path + p.filename, local_parent_path / Path(p.filename))
                # print((p.filename, remote_path , local_path))
            else:
                new_file = local_parent_path / p.filename
                with open(new_file, 'wb') as fp:
                    con.retrieveFile(share, parent_path + p.filename, fp)
                # print( "copied {0} to {1}".format( parent_path + p.filename, new_file) )


@task(max_retries=1, retry_delay=timedelta(seconds=1))
def fetch_remote_data(ip, port, user, password, local_name, remote_name, domain, share, remote_path, local_path):
    con = SMBConnection.SMBConnection(user, password, local_name, remote_name, domain)

    # while (not is_connected) and port < 500:
    #     try:
    #         is_connected = con.connect(ip, port=445, timeout=60)
    #     except ConnectionRefusedError:
    #         pass
    #     port = port + 1
    assert con.connect(ip, port=port, timeout=60)
    print("using port {}".format(port))
    smb_copy_folder(con, share, remote_path, local_path)
    con.close()
    return local_path
