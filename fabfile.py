from fabric.api import *
import os
from fabric.contrib import files
from fabric.context_managers import cd, lcd, shell_env
import tarfile

env.build_dir = os.getenv("FABFILE_DIR", os.path.dirname(os.path.abspath(__file__)))
env.build_venv_path = os.getenv("BUILD_VENV", os.path.join(env.build_dir, "env"))
env.build_venv_name = os.getenv("BUILD_VENV_NAME", "")
env.deploy_dir = os.getenv("DEPLOY_DIR", os.path.join("/var", "www", "up3ds"))
env.deploy_venv = os.getenv("DEPLOY_VENV", os.path.join("/var", "www", "venv", "up3ds"))
env.build_id = os.getenv("JBUILD_ID", "1")
env.deploy_to = os.getenv("DEPLOY_NAME", "prod")


def activate():
    return prefix("source %s" % os.path.join(env.build_venv_path, env.build_venv_name,
                                             "bin", "activate"))


def remote_activate():
    return prefix("source %s" % os.path.join(env.deploy_venv, "bin", "activate"))


def lmanage(postfix):
    with lcd(env.build_dir):
        with activate():
            with shell_env(DJANGO_SETTINGS_MODULE="up3ds.settings_prod"):
                local("%s/manage.py %s" % (env.build_dir, postfix))


def create_venv():
    """
    Create virtualenv if doesn't exist and install actual requirements
    """
    if not os.path.exists(env.build_venv_path):
        os.makedirs(env.build_venv_path)
        with lcd(env.build_venv_path):
            local("python3 -m venv %s" % env.build_venv_name)
    with activate():
        with lcd(env.build_dir):
            local("pip install -r requirements.txt --no-cache-dir")


def update_remote_venv():
    with remote_activate():
        with cd(os.path.join(env.deploy_dir, "current")):
            run("pip install -r requirements.txt --no-cache-dir")


def build_static():
    with lcd(os.path.join(env.build_dir, "client")):
        local("npm install --no-optional")
    with lcd(os.path.join(env.build_dir, "client", "backend")):
        local("gulp prod")
        local("gulp prod-compress")
    with lcd(os.path.join(env.build_dir, "client", "frontend")):
        local("gulp prod")
        local("gulp prod-compress")


def collect_static():
    lmanage("collectstatic --noinput --clear")


def prepare_tarball():
    print("Preparing tarball...")
    def filter_names(tarinfo):
        """
        Args:
            tarinfo (tarfile.TarInfo): tar info

        """
        name = tarinfo.name
        if tarinfo.isdir():
            if "media" in name or "client" in name:
                return None
        return tarinfo if ".pyc" not in name else None

    with lcd(env.build_dir):
        with tarfile.open(os.path.join(env.build_dir, "build.tar.gz"), "w:gz") as tar:
            tar.add(env.build_dir, arcname=".", recursive=True, filter=filter_names)
        pass


def build():
    create_venv()
    # build_static()
    collect_static()
    prepare_tarball()


def upload():
    print("Uploading build...")
    build_name = "BUILD-" + str(env.build_id)
    with cd(env.deploy_dir):
        if  files.exists(os.path.join(env.deploy_dir, build_name)):
            run("rm -rf " + os.path.join(env.deploy_dir, build_name))
        put(os.path.join(env.build_dir, "build.tar.gz"), env.deploy_dir)
        run("mkdir %s" % build_name)
        run("tar -xzf build.tar.gz -C %s" % build_name)
        run("rm -f build.tar.gz")
        run("ln -fsn ./%s/ ./current" % build_name)


def change_symlink():
    build_name = "BUILD-" + str(env.build_id)
    with cd(env.deploy_dir):
        run("ln -fsn ./%s/ ./current" % build_name)


def migrate():
    with remote_activate():
        with cd(os.path.join(env.deploy_dir, "current")):
            with prefix("export DJANGO_SETTINGS_MODULE=up3ds.settings_%s" % env.deploy_to):
                run("python manage.py migrate")


def deploy():
    upload()
    update_remote_venv()
    change_symlink()
    migrate()
    run("sudo systemctl restart uwsgi")
    run("sudo systemctl restart nginx")