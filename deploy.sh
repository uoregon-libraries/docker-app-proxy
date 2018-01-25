#!/bin/bash
set -eu

hostname=${1:-}
depdir=${2:-/usr/local/register}

if [[ $hostname == "" ]]; then
  echo "You must specify hostname!  (e.g., staging.blah.com)"
  echo
  echo "Usage: $0 <hostname> [deploy dir]"
  exit 1
fi

sudo rsync ./* $depdir/
sudo sed -i "s|^cd.*$|cd $depdir|" $depdir/register-app
sudo sed -i "s|%hostname%|$hostname|g" $depdir/nginx.tmpl
sudo sed -i "s|%hostname%|$hostname|g" $depdir/configure_service.py
sudo rm -f /usr/local/bin/register-app
sudo rm -f /usr/local/bin/setup-dc-staging
sudo cp $depdir/register-app /usr/local/bin/register-app
sudo cp $depdir/setup-dc-staging /usr/local/bin/setup-dc-staging
