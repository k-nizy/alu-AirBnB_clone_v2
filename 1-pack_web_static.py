#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    """
    try:
        # Create versions folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        
        # Create timestamp for archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        
        # Create the tar archive
        local("tar -cvzf {} web_static".format(archive_name))
        
        # Check if archive was created successfully
        if os.path.exists(archive_name):
            return archive_name
        else:
            return None
    except Exception:
        return None
