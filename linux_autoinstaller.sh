#!/bin/bash

if [ `uname -s` != 'Linux' ]
then
    echo "Must be a Linux system! Exiting..."
    exit 1
fi

apt-get install build-essential python-dev libmysqlclient-dev

sudo apt-get install python-setuptools python-dev build-essential libmysqlclient-dev python-pip
apt-get install libmysqlclient-dev python-dev
sudo pip install -U pip
sudo apt-get install mysql-server
sudo pip install MySQL-python
sudo pip install IMDbPY
sudo pip install tmdb3
sudo pip install HTML

/usr/bin/firefox https://central.github.com/mac/latest


cd
echo "alias gitcom='git commit -m "Commiting Changes"'" >> ~/.bashrc
echo "alias gitpull='git pull'" >> ~/.bashrc
echo "alias gitpush='git push --repo https://silversunseven:H4ck3r2b1@github.com/silversunseven/happyhome.git'" >> ~/.bashrc
echo "alias gitclone='git clone https://github.com/silversunseven/happyhome.git'" >> ~/.bashrc
echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
echo "export LANG=en_US.UTF-8" >> ~/.bashrc
echo "export MYSQL_HOME=/usr/local/mysql" >> ~/.bashrc
echo "alias mysqlstart='sudo /etc/init.d/mysql start'" >> ~/.bashrc
echo "alias mysqlstop='sudo /etc/init.d/mysql stop'" >> ~/.bashrc

#sudo  /usr/local/mysql/bin/mysqld stop
#touch /tmp/mysql.sock
sudo /etc/init.d/mysql start
echo "enter db pwd"
read passwd
echo "Setting DB root pwd to : $passwd"
mqysqladmin -u root password $passwd
/usr/bin/mysqladmin -p create imdb

/usr/bin/mysqladmin -u root password
#/usr/bin/mysqladmin -u root -p

/usr/bin/mysqladmin -p create imdb

git config --global user.email "silversunseven@gmail.com"
git config --global user.name "Aiden"

cd
mkdir project
cd project
gitclone


mkdir imdb_interface_files
cd imdb_interface_files/
ftp ftp://ftp.fu-berlin.de/pub/misc/movies/database/



_______
#  /usr/local/mysql/bin/mysqladmin -p create imdb
#  sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib
#  imdbpy2sql.py  -d /Users/aiden/project/happyhome/imdb_interface_files/ --mysql-force-myisam -u mysql://root:f4tb33@localhost/imdb
#
#
#
#dl and install https://mac.github.com/
#dl http://www.decalage.info/python/html#attachments
#cp /Users/aiden/Downloads/HTML.py-0.04.zip ../project/happyhome/
#cd ../project/happyhome/
#unzip HTML.py-0.04.zip
#cp HTML.py-0.04/HTML.py .
#
#add to .bashrc
#alias gitcom='git commit -m "Commiting Changes"'
#alias gitpull='git pull'
#alias gitpush='git push --repo https://silversunseven:H4ck3r2b1@github.com/silversunseven/happyhome.git'
#alias gitclone='git clone https://github.com/silversunseven/happyhome.git'
#export LC_ALL=en_US.UTF-8
#export LANG=en_US.UTF-8
#export MYSQL_HOME=/usr/local/mysql
#alias mysqlstart='sudo /usr/local/mysql/support-files/mysql.server start'
#alias mysqlstop='sudo /usr/local/mysql/support-files/mysql.server stop'
#
#git config --global user.email "silversunseven@gmail.com"
#git config --global user.name "Aiden
#mkdir project
#cd project
#gitclone
#
#
#
#mkdir imdb_interface_files
#cd imdb_interface_files/
#ftp ftp://ftp.fu-berlin.de/pub/misc/movies/database/
#hash
#mget *
#y
