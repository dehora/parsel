import paramiko


def create_sftp(host, ssh_username, key_file_path):
    #noinspection PyTypeChecker
    transport = paramiko.Transport((host, 22))
    key = paramiko.RSAKey.from_private_key_file(key_file_path)
    transport.connect(username=ssh_username, pkey=key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp
