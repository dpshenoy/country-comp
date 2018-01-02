
# Country-Comp

This is a Docker-ized [bokeh server](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html) app. The app loads a self-contained copy of country data taken from the ["world" data set from pgFoundry](http://pgfoundry.org/frs/?group_id=1000150&release_id=366#world-world-1.0-title-content). It plots countries in an X-Y scatter plot, allowing for comparison on several measures such as Gross National Product versus Life Expectancy, with optional filtering by region and form of government.

## Prerequisites

The host machine must have [Docker](https://www.docker.com/) installed and running, and also have [docker-compose](https://docs.docker.com/compose/) installed. The app runs two containers. See the "service" section in the `docker-compose.yml` file. The service `bokeh-app` is the bokeh server app, to which the service `nginx` proxies connections using [Docker service discovery](https://docs.docker.com/docker-cloud/apps/service-links/#discovering-containers-on-the-same-service-or-stack). This allows the bokeh server app to be run with `docker-compose up` without needing to set host-machine-specific info in an `--allow-websocket-origin` flag when starting up the bokeh server app.

## Usage

__1. Build the Images__

On the host machine run the following make command: 
```
$ make build
```
The `make build` command uses **docker-compose** to build the images, which are called **countrycomp\_bokeh-app** and **countrycomp\_nginx**. The bokeh app image is built using the python:3.6-slim image from DockerHub, with the necessary python packages for running bokeh added onto it. The finished image size is about 570 MB. Do `docker images`; the newly created images should be at the top of the list.

__2. Run the Containers__

Start the two containers running with:
```
$ make up
```
The `make up` command starts the containers and issues a **docker ps** command to confirm their status. There won't be any ports info for the bokeh-app container since connections to it are proxied by nginx. Browse to port 5006 on the host. For example, if you are running the containers on a remote machine reachable on your network at 10.20.30.40 then browse to `http://10.20.30.40:5006` to use the app.

__3. Stop and Remove the Containers__

To stop the app:
```
$ make down
```
The `make down` command stops and removes (destroys) the containers. To start the app up again, bring up new containers with `make up`.

__4. Running Manually for Debugging / Adapting & Development__

The app can be run manually, for example to debug it or to adapt & develop it further. Instead of `make up`, start a container in the foreground with a port on the local machine mapped directly to it (no nginx proxying), open an interactive bash terminal on the container, and run the bokeh server locally in the foreground:
```
[git::master] $ docker run -it -p 5006:5006 countrycomp_bokeh-app bash
nobody@6a8bafaebbae:/app$ bokeh serve country-comp/
2017-12-12 03:29:03,999 Starting Bokeh server version 0.12.13 (running on Tornado 4.5.2)
2017-12-12 03:29:04,003 Bokeh app running at: http://localhost:5006/country-comp
2017-12-12 03:29:04,003 Starting Bokeh server with process id: 7
. . .
```
These commands run the app at `http://localhost:5006`. The server will log connection requests and other info to stdout within the bash session. (As of 2017 November, the bokeh server logs to stdout only, with [no obvious option to re-direct logging to a file](https://github.com/bokeh/bokeh/issues/6699).)

To increase or decrease the logging level, use `Ctrl-C` to stop the app and re-run with the `--log-level` flag set to a value other than the default value `info`. For example:
```
nobody@6a8bafaebbae:/app$ bokeh serve country-comp --log-level debug
```
To see all options for the `--log-level` flag, do `bokeh serve --help`. Generally I find the default log-level is sufficient for debugging programming errors.
