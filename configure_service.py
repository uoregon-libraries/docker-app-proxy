def print_menu(service):
  print("Configure %s:" % service["name"])
  print("")
  print("P) Set exposed port (currently %d)" % service["port"])
  h = service["host"]
  print("H) Set host prefix (currently %s; e.g., your URL will look like http://%s.%hostname%)" % (h, h))
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

    if val == "P":
      exposed_str = raw_input("What port will the container expose? ")

      try:
        exposed = int(exposed_str)
        service["port"] = exposed
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
