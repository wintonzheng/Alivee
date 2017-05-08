#!/bin/bash

sudo pip install virtualenv

export WORK_ENV=./.virtualenvs
export WORK_ENV_ACTIVATE=./.virtualenvs/bin/activate
mkdir -p $WORK_ENV
sudo rm -rf $WORK_ENV
virtualenv $WORK_ENV
source $WORK_ENV_ACTIVATE

sudo pip install Django==1.10
sudo pip install mysqlclient==1.3.10
sudo pip install mock==2.0.0
sudo pip install freezegun==0.3.8
sudo pip install pyflakes==1.5.0
sudo pip install pep8==1.7.0
sudo pip install requests==2.13.0
