#!/bin/bash

sudo pip install virtualenv

export WORK_ENV=./.virtualenvs
export WORK_ENV_ACTIVATE=./.virtualenvs/bin/activate
mkdir -p $WORK_ENV
sudo rm -rf $WORK_ENV
virtualenv $WORK_ENV
source $WORK_ENV_ACTIVATE

sudo pip install Django==1.10
