#!/bin/bash

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=superman
export APP_DB_USER
# Edit the following to change the password of the database that will be created:
APP_DB_PASS=superman_db_pass
export APP_DB_PASS

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=$APP_DB_USER
export APP_DB_NAME

# Update package list and upgrade all packages
apt-get update
apt-get -y upgrade

# Install git for version control, pip for install python packages
echo 'Installing curl, git, Python 3, and pip...'
sudo apt-get install curl git python3 python3-dev libpq-dev build-essential -y
curl -s https://bootstrap.pypa.io/get-pip.py | python3.4

# setup postgresql
cd /vagrant
sh Vagrant-setup/postgresql.sh

# Install virtualenv / virtualenvwrapper
echo 'Installing and configuring virtualenv and virtualenvwrapper...'
pip install --quiet virtualenvwrapper==4.7.0 Pygments==2.1.1
mkdir -p ~vagrant/.virtualenvs
chown vagrant:vagrant ~vagrant/.virtualenvs
printf "\n\n# Virtualenv settings\n" >> ~vagrant/.bash_profile
printf "export PYTHONPATH=/usr/lib/python3.4" >> ~vagrant/.bash_profile
printf "export WORKON_HOME=~vagrant/.virtualenvs\n" >> ~vagrant/.bash_profile
printf "export PROJECT_HOME=/vagrant\n" >> ~vagrant/.bash_profile
printf "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.4\n" >> ~vagrant/.bash_profile
printf "source /usr/local/bin/virtualenvwrapper.sh\n" >> ~vagrant/.bash_profile
printf "export DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:5432/$APP_DB_NAME\n" >> ~vagrant/.bash_profile

# Some useful aliases for getting started
echo 'Setting up message of the day, and some aliases...'
printf "\nUseful Aliases:\n"
printf "alias ccat='pygmentize -O style=monokai -f terminal -g'\n" >> ~vagrant/.bash_profile

# reload bash profile
echo 'Reloading bash profile...'
source ~vagrant/.bash_profile

echo 'Creating virtualenv...'
mkvirtualenv venv
echo 'Starting virtualenv...'
workon venv

echo 'Installing requirements...'
pip install -r requirements.txt

echo 'Running migrations...'
python manage.py migrate

echo 'Loading test data...'
python manage.py loaddata test_users

echo 'Starting django server...'
nohup python manage.py runserver 0.0.0.0:8000 &

# Complete
echo ""
echo "Vagrant install complete."
echo "Now try logging in:"
echo "    $ vagrant ssh"
echo "Django development server running at:"
echo "    http://localhost:8000"
