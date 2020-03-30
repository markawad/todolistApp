import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, sudo

REPO_URL = 'https://github.com/markawad/todolistApp.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'

    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _create_nginx_file()
        _create_systemd_service()
        _start_servers()

# This allows us to get the most recent source code from our repo
def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} ../{env.host}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

# Updating our env variables file
def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y') # Adds to file if does not exist
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        secret_key = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={secret_key}')
    
def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')

def _create_nginx_file():
    if not exists(f'/etc/nginx/sites-available/{env.host}'):
        sudo(f'cat ./deploy_tools/nginx.template.conf | \
            sed "s/DOMAIN/{env.host}/g" | \
            tee /etc/nginx/sites-available/{env.host}')
        sudo(f'ln -s /etc/nginx/sites-available/{env.host} \
            /etc/nginx/sites-enabled/{env.host}')

def _create_systemd_service():
    if not exists(f'/etc/systemd/system/gunicorn-{env.host}.service'):
        sudo(f'cat ./deploy_tools/gunicorn-systemd.template.service | \
            sed "s/DOMAIN/{env.host}/g" | \
            tee /etc/systemd/system/gunicorn-{env.host}.service')

def _start_servers():
    sudo('systemctl daemon-reload')
    sudo('nginx -s reload')
    sudo(f'systemctl enable gunicorn-{env.host}')
    sudo(f'systemctl start gunicorn-{env.host}')