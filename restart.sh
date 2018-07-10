#!/usr/bin/env bash

git pull origin master

sudo supervisorctl restart tornado-1
