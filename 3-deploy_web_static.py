#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, local, run, put
from datetime import datetime
import os

# Define your web servers here
env.hosts = ['54.157.32.137', '52.55.249.213']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Update with your SSH key path


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        
        local("tar -cvzf {} web_static".format(archive_name))
        
        if os.path.exists(archive_name):
            return archive_name
        else:
            return None
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.replace('.tgz', '')
        folder_path = '/data/web_static/releases/{}/'.format(folder_name)

        run('sudo mkdir -p {}'.format(folder_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_filename, folder_path))
        run('sudo rm /tmp/{}'.format(archive_filename))
        run('sudo mv {}web_static/* {}'.format(folder_path, folder_path))
        run('sudo rm -rf {}web_static'.format(folder_path))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(folder_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    # Pack the web_static content
    archive_path = do_pack()
    
    if archive_path is None:
        print("Packing failed!")
        return False
    
    print("web_static packed: {} -> {}Bytes".format(
        archive_path, 
        os.path.getsize(archive_path) if os.path.exists(archive_path) else 0
    ))
    
    # Deploy the archive
    return do_deploy(archive_path)
