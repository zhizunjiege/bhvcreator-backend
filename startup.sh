#!/bin/bash

# parse arguments -w, -l
while getopts "w:l:" opt; do
  case $opt in
  w)
    workers=$OPTARG
    ;;
  l)
    loglevel=$OPTARG
    ;;
  ?)
    echo "Invalid option: -$opt"
    ;;
  esac
done

function grace_exit() {
  echo "graceful exiting..."
  for process in "$@"; do
    echo "kill $process"
    kill -TERM $(ps -ef | grep $process | grep -v grep | awk '{print $2}')
  done
  echo "graceful exited"
  exit 0
}

trap "grace_exit gunicorn" INT TERM

# mkdir for logs
mkdir -p data/logs

# get current time
time=$(date +"%Y-%m-%d %H-%M-%S")

# run gunicorn in background
echo "starting gunicorn..."
gunicorn -w ${workers:-4} -b 0.0.0.0:80 --log-level ${loglevel:-error} --preload app:app </dev/null >"data/logs/$time.app.log" 2>&1 &

# wait for subprocess
wait
