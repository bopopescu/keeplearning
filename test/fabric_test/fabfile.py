from fabric.api import run
from fabric.api import env

env.use_ssh_config = True
env.ssh_config_path = '/root/.ssh/config'

def host_type():
    run('touch /tmp/test1.txt')