#!/bin/bash
# Builds the Drive file index and deploys the MATH module review portal to Firebase Hosting.
# Run from Cloud Shell:  bash <(curl -fsSL https://raw.githubusercontent.com/smartpathtutordev/mit-dit-courses/math-review-portal/deploy.sh)
set -euo pipefail
P=${P:-smartpath-math-review}
SITE=${SITE:-smartpath-math-review}
RAW=https://raw.githubusercontent.com/smartpathtutordev/mit-dit-courses/math-review-portal
export GOOGLE_CLOUD_QUOTA_PROJECT=$P
gcloud config set project "$P" >/dev/null 2>&1
gcloud config set billing/quota_project "$P" >/dev/null 2>&1 || true
mkdir -p ~/mathportal/public && cd ~/mathportal
for f in index.html sw.js config.js vault.js; do curl -fsSL "$RAW/$f?$(date +%s)" -o "public/$f"; done
curl -fsSL "$RAW/build_manifest.py?$(date +%s)" -o build_manifest.py
curl -fsSL "$RAW/encrypt.js?$(date +%s)" -o encrypt.js
cat > firebase.json <<EOF
{ "hosting": { "site": "$SITE", "public": "public",
  "headers": [ { "source": "**/*.@(js|html|json)", "headers": [ { "key": "Cache-Control", "value": "no-cache" } ] } ] } }
EOF
if [ ! -s ~/mathportal/.key ]; then
  echo "== creating api key"
  gcloud services enable drive.googleapis.com apikeys.googleapis.com
  gcloud services api-keys create --display-name="Math module review portal" \
    --api-target=service=drive.googleapis.com \
    --allowed-referrers="https://$SITE.web.app/*,https://$SITE.firebaseapp.com/*" --format=json > ~/mathportal/.keyop.json
  python3 -c "import json;d=json.load(open('$HOME/mathportal/.keyop.json'));print((d.get('response') or d).get('keyString',''))" > ~/mathportal/.key
fi
KEY=$(cat ~/mathportal/.key)
[ -n "$KEY" ] || { echo "NO KEY"; exit 1; }
sed -i "s#apiKey: \"\"#apiKey: \"$KEY\"#" public/config.js
if [ "${SKIP_BUILD:-0}" != "1" ]; then
  echo "== building file index from Drive"
  rm -rf public/m public/tree.json
  NAV_ONLY="${NAV_ONLY:-1}" python3 build_manifest.py public/config.js public "https://$SITE.web.app/"
fi
echo "== locking with the portal password"
[ -s ~/mathportal/.password ] || { echo "Put the portal password in ~/mathportal/.password first"; exit 1; }
[ -s ~/mathportal/.salt ] || openssl rand -base64 16 > ~/mathportal/.salt
node encrypt.js public "$(cat ~/mathportal/.password)" "$(cat ~/mathportal/.salt)"
echo "== deploy"
curl -fsSL "$RAW/redeploy.sh?$(date +%s)" -o redeploy.sh && P="$P" bash redeploy.sh
echo "DONE https://$SITE.web.app"
