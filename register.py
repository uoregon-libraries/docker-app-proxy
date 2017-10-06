#!/usr/bin/python
#
# register.py allows registering a directory as a proxyable nginx application

import os
import sys
import yaml

def usage(err = ""):
  exitcode=0
  if err != "":
    exitcode=1
    print("ERROR: %s" % err)
    print("")

  print("Usage: %s <docker directory>" % sys.argv[0])
  sys.exit(exitcode)

def getcli():
  """Checks args and prints errors as needed, returning the compose file we'll
  use for this operation"""

  if len(sys.argv) < 2:
    usage("You must specify a directory")

  if len(sys.argv) > 2:
    usage("You may only specify one directory at a time")

  dirname = os.path.abspath(sys.argv[1])

  if not os.path.isdir(dirname):
    usage("Invalid directory name: %s" % dirname)

  fname = os.path.join(dirname, "docker-compose.yml")

  if not os.path.isfile(fname):
    usage("Unable to find docker-compose.yml file in %s" % dirname)

  return dirname, fname

def load_yaml(fname):
  """Open the given file and return its yaml data structure(s)"""
  with open(fname, "r") as f:
    data = f.read()
  return yaml.load(data)

def hack_data(data):
  """Fix up the compose structure for our staging needs"""
  for service_name in data["services"].iterkeys():
    data["services"][service_name].pop("ports", None)

def write_staging_compose(data, dirname):
  """Write the given config to a staging-specific compose file"""
  fname = os.path.join(dirname, "staging.docker-compose.yml")
  with open(fname, "w") as f:
    f.write(yaml.dump(data, default_flow_style=False))

def get_service_metadata(service):
  print("Not implemented")
  print("")

def menu(services):
  print("Choose which service(s) to expose:")
  print("")
  num_map = {}
  optnum = 1
  for service in services:
    print("%d) %s" % (optnum, service))
    num_map["%d" % optnum] = service
    optnum += 1

  print("")
  print("A) Abort (exit without saving)")
  print("X) Save and exit (will reload nginx)")
  print("")

  done = False
  while not done:
    try:
      val = raw_input(">> ").upper()
    except EOFError:
      print("")
      val = "A"

    if val in num_map:
      get_service_metadata(num_map[val])
      continue

    if val == "A":
      print("Aborting")
      print("")
      return

    if val == "X":
      print("Not implemented!  Use 'A' to abort for now.")
      print("")
      continue

    print("Invalid option")
    print("")

def main():
  dirname, compose_file = getcli()
  data = load_yaml(compose_file)
  hack_data(data)
  write_staging_compose(data, dirname)
  menu(data["services"].iterkeys())

if __name__ == '__main__':
  main()
