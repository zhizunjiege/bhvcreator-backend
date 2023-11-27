#!/bin/bash

# parse arguments -w, -l
while getopts "w:" opt; do
  case $opt in
  w)
    workers=$OPTARG
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

trap "grace_exit waitress-serve" INT TERM

# mkdir for logs
mkdir -p data/logs

# get current time
time=$(date +"%Y-%m-%d %H-%M-%S")

# run waitress in background
echo "starting waitress..."
waitress-serve --listen 0.0.0.0:6666 --threads=${workers:-4} app:app </dev/null >"data/logs/$time.app.log" 2>&1 &

# wait for subprocess
wait
