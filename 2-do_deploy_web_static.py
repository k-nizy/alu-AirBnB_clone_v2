#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run, sudo
import os

# Define your web servers here
env.hosts = ['54.157.32.137', '52.55.249.213']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Update with your SSH key path


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, '/tmp/')

        # Get archive filename without extension
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.replace('.tgz', '')
        folder_path = '/data/web_static/releases/{}/'.format(folder_name)

        # Create target directory
        run('sudo mkdir -p {}'.format(folder_path))

        # Uncompress archive to target directory
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_filename, folder_path))

        # Remove archive from /tmp/
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Move contents to proper location
        run('sudo mv {}web_static/* {}'.format(folder_path, folder_path))

        # Remove empty web_static directory
        run('sudo rm -rf {}web_static'.format(folder_path))

        # Delete existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create new symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(folder_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False
