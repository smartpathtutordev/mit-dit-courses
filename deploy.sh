#!/bin/bash
# Deploys the MATH module review portal to Firebase Hosting from Cloud Shell.
set -euo pipefail
P=gen-lang-client-0836239265
SITE=${SITE:-smartpath-math-review}
RAW=https://raw.githubusercontent.com/smartpathtutordev/mit-dit-courses/math-review-portal
gcloud config set project "$P" >/dev/null
echo "== enabling APIs"
gcloud services enable drive.googleapis.com apikeys.googleapis.com firebase.googleapis.com firebasehosting.googleapis.com
mkdir -p ~/mathportal/public && cd ~/mathportal
for f in index.html sw.js config.js; do curl -fsSL "$RAW/$f?$(date +%s)" -o "public/$f"; done
cat > firebase.json <<EOF
{ "hosting": { "site": "$SITE", "public": "public",
  "headers": [ { "source": "**/*.@(js|html)", "headers": [ { "key": "Cache-Control", "value": "no-cache" } ] } ] } }
EOF
echo "== firebase project"
firebase projects:list 2>/dev/null | grep -q "$P" || firebase projects:addfirebase "$P"
echo "== hosting site"
firebase hosting:sites:get "$SITE" --project "$P" >/dev/null 2>&1 || firebase hosting:sites:create "$SITE" --project "$P"
echo "== api key"
if [ ! -s ~/mathportal/.key ]; then
  gcloud services api-keys create --display-name="Math module review portal" \
    --api-target=service=drive.googleapis.com \
    --allowed-referrers="https://$SITE.web.app/*,https://$SITE.firebaseapp.com/*" --format=json > ~/mathportal/.keyop.json
  python3 -c "import json;d=json.load(open('$HOME/mathportal/.keyop.json'));print((d.get('response') or d).get('keyString',''))" > ~/mathportal/.key
fi
KEY=$(cat ~/mathportal/.key)
[ -n "$KEY" ] || { echo "NO KEY"; exit 1; }
sed -i "s#apiKey: \"\"#apiKey: \"$KEY\"#" public/config.js
echo "== deploy"
firebase deploy --only hosting --project "$P" --non-interactive
echo "DONE https://$SITE.web.app"
