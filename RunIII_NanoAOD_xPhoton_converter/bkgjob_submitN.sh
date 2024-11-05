#!/usr/bin/env sh

nJOBs=${1:-5}
sleepTIME=${2:-3}
function check_submitted_jobs {
  # Count the number of active background jobs
  while [ "$(jobs -r | wc -l)" -ge "$nJOBs" ]; do
    # Wait for one of the background jobs to complete before starting another one
    sleep $sleepTIME
  done
}

check_submitted_jobs
