-- Install pip, git
sudo apt-get install pip
sudo apt-get install git
sudo apt-get install realpath   -- Need for run script from independent directory.
sudo apt-get install python-mysqldb

-- Install scrapy
sudo pip install scrapy

-- Clone (cd to desired directory before)
git clone https://github.com/kirimaks/fetch_pages.git

-- Addition (if something wrong)
sudo pip install pyasn1 --upgrade
sudo pip install service_identity
