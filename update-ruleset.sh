#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Updating sing-geosite submodule to latest rule-set..."
git submodule update --init --recursive
git submodule update --remote --merge sing-geosite

echo "Done."
