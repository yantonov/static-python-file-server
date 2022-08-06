#!/usr/bin/env bash
set -o errexit -o nounset

curl -v 'http://localhost:8080/some-url-with-parameter?p=1&q=2'
