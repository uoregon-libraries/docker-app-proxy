#!/usr/bin/python
#
# register.py allows registering a directory as a proxyable nginx application

import json
import os
import sys
import yaml
import configure_service

STAGING_FILE_BASE="docker-compose.staging.yml"

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

def staging_file(dirname):
  return os.path.join(dirname, STAGING_FILE_BASE)

def has_staging_compose(dirname):
  return os.path.exists(staging_file(dirname))

def apply_service_confs(data, confs):
  """Return the service config information from environment variables configured in data"""
  for name, dockerdata in data["services"].iteritems():
    if name not in confs:
      confs[name] = {"name": name, "port": 0, "host": name}

    if "environment" not in dockerdata:
      continue

    env = dockerdata["environment"]
    for var in env:
      parts = var.split("=", 1)
      if len(parts) != 2:
        continue

      key, val = parts[0], parts[1]
      if key == "STGCONF_X_PORT":
        confs[name]["port"] = int(val)
      if key == "STGCONF_X_HOST":
        confs[name]["host"] = val

def write_staging_compose(dirname, data, confs):
  """Write the given config to a staging-specific compose file"""
  for name, conf in confs.iteritems():
    dockerdata = data["services"][name]
    if conf["port"] > 0:
      if "environment" not in dockerdata:
        dockerdata["environment"] = []
      dockerdata["environment"].append("STGCONF_X_PORT=%d" % conf["port"])
      dockerdata["environment"].append("STGCONF_X_HOST=%s" % conf["host"])

  with open(staging_file(dirname), "w") as f:
    f.write(yaml.dump(data, default_flow_style=False))

def print_menu(services, confs):
  print("Choose which service(s) to expose:")
  print("")
  optnum = 1
  for service in services:
    conf = confs[service]
    if conf["port"] > 0:
      print("%d) %s [host: %s; port: %d]" % (optnum, service, conf["host"], conf["port"]))
    else:
      print("%d) %s [not exposed]" % (optnum, service))
    optnum += 1
  print("")
  print("A) Abort (exit without saving)")
  print("X) Save and exit (will reload nginx)")
  print("")

def main_menu(confs):
  svc_list = []
  for service in confs.iterkeys():
    svc_list.append(service)

  print_menu(svc_list, confs)

  done = False
  while not done:
    try:
      val = raw_input(">> ").upper()
    except EOFError:
      print("")
      val = "A"

    try:
      valnum = int(val)
      if valnum < len(svc_list):
        service = svc_list[valnum-1]
        configure_service.run(confs[service])
        print_menu(svc_list, confs)
        continue
    except ValueError:
      pass

    if val == "A":
      print("Aborting")
      print("")
      return None

    if val == "X":
      print("Saving data and writing out to staging compose file")
      return confs

    print("Invalid option")
    print_menu(svc_list, confs)

def main():
  dirname, compose_file = getcli()
  data = load_yaml(compose_file)
  hack_data(data)
  confs = {}
  apply_service_confs(data, confs)
  if has_staging_compose(dirname):
    staging_data = load_yaml(staging_file(dirname))
    apply_service_confs(staging_data, confs)

  final_confs = main_menu(confs)
  if final_confs is not None:
    print("You can now cd to %s and run docker-compose with the staging file (%s)" % (dirname, STAGING_FILE_BASE))
    write_staging_compose(dirname, data, final_confs)

if __name__ == '__main__':
  main()
