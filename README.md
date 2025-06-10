python3 -m venv env/
source env/bin/activate

pip install -r requirements.txt

sudo apt update
sudo apt install -y python3 python3-pip

sudo apt install -y sqlite3 libsqlite3-dev

sudo apt update
sudo apt install python3-pip
pip3 install --upgrade pip setuptools

pip3 install adafruit-circuitpython-ads1x15
