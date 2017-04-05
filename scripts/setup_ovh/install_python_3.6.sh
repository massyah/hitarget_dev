wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
tar xvf Python-3.6.0.tgz
cd Python-3.6.0
./configure --enable-optimizations
make -j8
sudo make altinstall
python3.6