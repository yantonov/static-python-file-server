#!/usr/bin/env bash
set -o errexit -o nounset

cd "$(dirname "$0")/.."

python3 server.py
