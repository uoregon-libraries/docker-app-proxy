def print_menu(service):
  print("Configure %s:" % service["name"])
  print("")
  print("C) Clear exposed ports")
  print("P) Map a port (current mappings: %s)" % repr(service["ports"]))
  h = service["host"]
  print("H) Set host prefix (currently %s; e.g., your final URL might look like http://%s.staging.domain.com)" % (h, h))
  print("")
  print("A) Abort and return to main menu")
  print("X) Save and return to main menu")
  print("")

def run(service):
  done = False
  print_menu(service)
  while not done:
    try:
      val = raw_input(">> ").upper()
    except EOFError:
      print("")
      val = "A"

    if val == "C":
      service["ports"] = {}
      print("Cleared all port mappings")
      print("")
      continue

    if val == "P":
      exposed_str = raw_input("What port will the container expose? ")
      nginx_str = raw_input("What port will nginx route from the outside world? ")

      if nginx_str != "80" and nginx_str != "443":
        print("You can only map ports 80 and/or 443")
        continue

      try:
        exposed = int(exposed_str)
        nginx = int(nginx_str)
        service["ports"][nginx] = exposed
      except ValueError:
        print("Invalid port value(s); nothing mapped")

      print("")
      continue

    if val == "H":
      host = raw_input("What would you like the hostname to be? ")
      if "." in host:
        print("Invalid hostname; no changes made")
      else:
        service["host"] = host

      print("")
      continue

    if val == "A":
      print("Changes aborted; returning to main menu")
      print("")
      return

    if val == "X":
      print("Changes saved; returning to main menu")
      print("")
      return

    print("Invalid option")
    print_menu(service)
