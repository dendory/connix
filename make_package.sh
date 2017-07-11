#!/bin/bash
python3 -c "import connix;help(connix.connix)" > README.txt
python3 setup.py sdist
twine upload dist/*
rm -rf dist
sudo pip3 install connix --upgrade
git add *
git commit -m "updates"
git push
