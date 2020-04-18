#!/usr/bin/env bash
eval $(ssh-agent -s)
if [ -d "7_trinhvt" ]; then
  cd 7_trinhvt
  git pull origin master
else
  git clone "git@gitlab.com:is_soict/it4434_20192/7_trinhvt.git"
fi
