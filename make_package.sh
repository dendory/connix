#!/bin/bash
python3 -c "import connix;help(connix.connix)" > README.txt
python3 setup.py sdist
twine upload dist/*
rm -rf dist
rm -rf connix.egg-info/
rm -rf connix/__pycache__
git add .
git commit -m "new release"
git push
sudo pip3 install connix --upgrade
