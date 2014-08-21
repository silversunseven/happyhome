#!/bin/bash

if `uname -s` != 'Darwin'
then
    echo "Must be a mac system! Exiting..."
    exit 1
fi

sudo easy_install pip
sudo easy_install -U setuptools
sudo easy_install -U mysqladmin
sudo easy_install mysql-python
sudo pip install IMDbPY
sudo pip install tmdb3
sudo pip install HTML

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.20-osx10.8-x86_64.dmg
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome https://central.github.com/mac/latest
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome http://www.decalage.info/files/HTML.py-0.04.zip

cd
echo "alias gitcom='git commit -m "Commiting Changes"'" >> .bashrc
echo "alias gitpull='git pull'" >> .bashrc
echo "alias gitpush='git push --repo https://silversunseven:H4ck3r2b1@github.com/silversunseven/happyhome.git'" >> .bashrc
echo "alias gitclone='git clone https://github.com/silversunseven/happyhome.git'" >> .bashrc
echo "export LC_ALL=en_US.UTF-8" >> .bashrc
echo "export LANG=en_US.UTF-8" >> .bashrc
echo "export MYSQL_HOME=/usr/local/mysql" >> .bashrc
echo "alias mysqlstart='sudo /usr/local/mysql/support-files/mysql.server start'" >> .bashrc
echo "alias mysqlstop='sudo /usr/local/mysql/support-files/mysql.server stop'" >> .bashrc

#sudo  /usr/local/mysql/bin/mysqld stop
#touch /tmp/mysql.sock
sudo /usr/local/mysql/support-files/mysql.server start
mysqladmin -u root password

/usr/local/mysql/bin/mysqladmin -p create imdb
sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib

git config --global user.email "silversunseven@gmail.com"
git config --global user.name "Aiden
cd
mkdir project
cd project
gitclone


mkdir imdb_interface_files
cd imdb_interface_files/
ftp ftp://ftp.fu-berlin.de/pub/misc/movies/database/



_______
sudo easy_install pip
python
sudo easy_install -U setuptools
sudo easy_install -U mysqladmin
sudo easy_install mysql-python
sudo pip install IMDbPY
sudo pip install tmdb3
sudo pip install HTML

dl mysql-5.6.20-osx10.dmg from http://dev.mysql.com/downloads/mysql/  (...help: http://dev.mysql.com/doc/refman/5.0/en/macosx-installation.html)
install dmg
  sudo  /usr/local/mysql/bin/mysqld stop
  touch /tmp/mysql.sock
  sudo  /usr/local/mysql/bin/mysqld_safe restart
  sudo /usr/local/mysql/support-files/mysql.server start
  mysqladmin -u root password
  mysql>    EXIT
  /usr/local/mysql/bin/mysqladmin -p create imdb
  sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib
  imdbpy2sql.py  -d /Users/aiden/project/happyhome/imdb_interface_files/ --mysql-force-myisam -u mysql://root:f4tb33@localhost/imdb



dl and install https://mac.github.com/
dl http://www.decalage.info/python/html#attachments
cp /Users/aiden/Downloads/HTML.py-0.04.zip ../project/happyhome/
cd ../project/happyhome/
unzip HTML.py-0.04.zip
cp HTML.py-0.04/HTML.py .

add to .bashrc
alias gitcom='git commit -m "Commiting Changes"'
alias gitpull='git pull'
alias gitpush='git push --repo https://silversunseven:H4ck3r2b1@github.com/silversunseven/happyhome.git'
alias gitclone='git clone https://github.com/silversunseven/happyhome.git'
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export MYSQL_HOME=/usr/local/mysql
alias mysqlstart='sudo /usr/local/mysql/support-files/mysql.server start'
alias mysqlstop='sudo /usr/local/mysql/support-files/mysql.server stop'

git config --global user.email "silversunseven@gmail.com"
git config --global user.name "Aiden
mkdir project
cd project
gitclone



mkdir imdb_interface_files
cd imdb_interface_files/
ftp ftp://ftp.fu-berlin.de/pub/misc/movies/database/
hash
mget *
y