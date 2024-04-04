#!/usr/bin/python3

"""This fabric script generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo."""

from datetime import datetime
from fabric.api import local
from fabric.api import env
from fabric.api import run
from fabric.api import put

env.hosts = ["web-01.lzcorp.tech", "web-02.lzcorp.tech"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/alx-server-key.pem"


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {file_path} web_static")
        return file_path
    except IOError:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    try:
        archive_name = archive_path.split("/")[-1]
        archive_name_no_ext = archive_name.split(".")[0]
        put(archive_path, "/tmp/")

        run(f"mkdir -p /data/web_static/releases/{archive_name_no_ext}/")
        run(
            f"tar -xzf /tmp/{archive_name} -C "
            f"/data/web_static/releases/{archive_name_no_ext}/"
        )
        run(f"rm /tmp/{archive_name}")
        run(
            f"mv /data/web_static/releases/{archive_name_no_ext}/web_static/* "
            f"/data/web_static/releases/{archive_name_no_ext}/"
        )
        run(
            "rm -rf "
            f"/data/web_static/releases/{archive_name_no_ext}/web_static"
        )
        run("rm -rf /data/web_static/current")
        run(
            f"ln -s /data/web_static/releases/{archive_name_no_ext}/ "
            "/data/web_static/current"
        )
        print("New version deployed!")
        return True
    except IOError:
        return False
