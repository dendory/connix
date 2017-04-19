#!/bin/bash
python3 -c "import connix;help(connix.connix)" > README.txt
python setup.py register -r pypi
python setup.py sdist upload -r pypi
sudo pip3 install connix --upgrade
