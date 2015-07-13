#!/bin/bash
# setup NGINX on 14.04 LTS to run Controversy
# run as root

cd ~

adduser deployer 
adduser deployer sudo

sudo apt-get install -y git

sudo apt-get update
sudo apt-get install -y gunicorn supervisor nginx python python-pip python-virtualenv python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose redis-server mysql-server

mkdir /home/www
cd /home/www

git clone https://github.com/gdyer/controversy
cd controversy/server
virtualenv --system-site-packages venv
. venv/bin/activate

sudo pip install -r requirements.txt

echo "import nltk
nltk.download('all')" > get-nltk.py
python get-nltk.py 
rm get-nltk.py

mv sample-config.py config.py

sudo /etc/init.d/nginx start
rm /etc/nginx/sites-enabled/default
touch /etc/nginx/sites-available/controversy
ln -s /etc/nginx/sites-available/controversy /etc/nginx/sites-enabled/controversy
mv controversy /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart

echo "[program:controversy]
command=gunicorn app:app -b localhost:8000 --log-file /var/log/gunicorn/log.log
directory=/home/www/controversy/server
user=root
stderr_logfile=/var/log/supervisor/error.log
stdout_logfile=/var/log/supervisor/out.log" > /etc/supervisor/conf.d/controversy.conf
supervisorctl reread
supervisorctl update
supervisorctl start controversy

echo "\tEnter your MySQL password, then: CREATE DATABASE controversy; USE controversy; SOURCE schema.sql;
\n\nAfterwards, be sure to edit server/config.py with correct credentials"
mysql -p
