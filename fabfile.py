__author__ = 'jackyun'
from fabric.api import *

def prepare_deploy():
    local("git add -p && git commit")
    local("git push")

env.hosts = ['54.249.52.200']
env.user = 'ec2-user'
env.key_filename = '/Users/jackyun/.ssh/tokyo_jack.pem'

def deploy():
    code_dir = '/home/ec2-user/smart-memorizer'
    with cd(code_dir):
        run("git pull")
