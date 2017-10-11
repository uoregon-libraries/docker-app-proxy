Docker App Register
===

This is a simple Python script we use at the UO Libraries for creating a
semi-automated staging server for docker-compose projects.

This project (and this documentation) is mostly for UO internally, so feel free
to use this as inspiration, but understand that if your staging server differs
significantly enough, you may need to significantly alter the nginx config, the
python, or both.

Setup
---

- Install docker and docker-compose
- Install nginx
- Grab [docker-gen](https://github.com/jwilder/docker-gen) and copy the binary to /usr/local/bin or something
- You may have to make SELinux more permissive if you have containers that expose arbitrary ports:
  - `setsebool -P httpd_can_network_connect on`
- Get docker-gen running (this will have to be done as root):
  - `/usr/local/bin/docker-gen --watch --notify "nginx -s reload" /usr/local/register/nginx.tmpl /etc/nginx/conf.d/docker.conf`
  - Feel free to submit a PR with a systemd setup (we'll probably get to this eventually)
- Put this project somewhere accessible by all users, such as
  /usr/local/register - or copy and modify the [register-app](./register-app)
  example script

Usage
---

### Automatic

Register an app that uses compose via `register-app <path to app>`.  This will
let you specify the app's hostname and which services are exposed by nginx as
well as which port in the container needs to be exposed on port 80.

Once you've saved your configuration and exited, you'll have a
`staging.docker-compose.yml` file which you can then use.  Assuming the
`docker-gen` watcher is working, simply starting up the stack with the staging
file will make everything "just work":

    docker-compose -f staging.docker-compose.yml up -d

### Manual

You can simply add environment variables to your services if you'd rather not
deal with the `register-app` script.  The current list of vars is as follows:

- `STGCONF_X_HOST`: This is the prefixed host nginx will use to expose your
  application.  If this is set to "foo", for instance, and the project was
  deployed with a hostname of "staging.bar.com", the full URL would be
  "http(s)://foo.staging.bar.com".
- `STGCONF_X_P80`: Specify the service's port which you want to be used when a
  request is made to http://[host]
- `STGCONF_X_P443` Specify the service's port which you want to be used when a
  request is made to https://[host]