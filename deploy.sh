#!/usr/bin/env bash

commitTime=`date '+%Y-%m-%d %H:%M:%S'`

git status

git pull origin master

git add --all

git commit -m "${commitTime} : Optimize system stability"

git push origin master
