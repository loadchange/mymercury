#!/bin/bash

function FileModify(){

  nmf=`find ./*  -mmin 0.01667 -exec du -sb {} \; |awk '{print $2}' `

  if [ ! "$nmf" = "" ]; then
    scpf="~/code/toy/"${nmf:18}
    echo "[$(date "+%Y-%m-%d %H:%M:%S")]文件修改:“"$nmf
    scp -P 22 -r $nmf wangyanmin@10.12.43.225:$scpf
  fi


  sleep 1s
  FileModify

}

FileModify