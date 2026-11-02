#!/bin/bash
# Re-runs the Firebase deploy until every file is uploaded (Cloud Shell uploads drop now and then).
cd ~/mathportal || exit 1
export NODE_OPTIONS=--dns-result-order=ipv4first
for i in $(seq 20); do
  if firebase deploy --only hosting --project smartpath-math-review --non-interactive > /tmp/fd.log 2>&1; then
    echo "DEPLOY-OK after $i tries"; exit 0
  fi
  echo "try $i: $(grep -o 'uploading new files[^)]*)' /tmp/fd.log | tail -1)"
done
echo DEPLOY-FAILED
