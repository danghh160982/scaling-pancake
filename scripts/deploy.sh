#!/usr/bin/env bash

eval $(ssh-agent -s)
if [ -d "7_trinhvt" ]; then
  cd 7_trinhvt
  git pull origin master
else
  git clone "git@gitlab.com:is_soict/it4434_20192/7_trinhvt.git"
  cd 7_trinhvt
fi

CURRENT_TIME=$(date +%Y-%m-%d__%H_%M_%S)
LOG_FILE=/tmp/project/project.uwsgi.log
[ -f ${LOG_FILE} ] && mv ${LOG_FILE} /tmp/project/project.uwsgi.${CURRENT_TIME}.log

MASTER_PROCESS=$(ps aux | grep uwsgi | grep -v grep | awk '{print $2}' | head -n 1)
[ ${MASTER_PROCESS} ] && kill -9 ${MASTER_PROCESS}

cd backend
whoami
pwd
/home/deploy/anaconda3/envs/project/bin/uwsgi project.ini
