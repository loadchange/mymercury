#!/usr/bin/env bash

git pull origin master

sudo supervisorctl restart tornados:tornado-0
