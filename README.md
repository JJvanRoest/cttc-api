# Setup

Assumed Linux/MacOS. For Windows, kindly use Windows Subsystem for Linux (WSL).

Required python version is 3.8.0. Support for other versions is not guaranteed.

Before starting; make sure you have access to a (postgres) database and API keys for the different services, see below.

## Setup configuration
First, setup the configurations:
```bash
cp config.json.example config.json
```
Edit the newly created config.json to your liking, make sure you have the correct API tokens for the 3rd party services (or enable test_mode, which should bypass the 3rd parties).

## Run directly (somewhat slower, much easier)
Setup the python dependencies and run locally. These commands should be ran one after the other.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The app is now accessible on `localhost:5000`. You can forward this port on  you local network or use a tunnel (e.g. Ngrok) to make the app accessible directly to the outside world.

## Docker
Depending on the setup:
- Set up traefik as a reverse proxy, make sure the labels are correct.
- Remove the labels for traefik and networks and add the snippet below to the app service instead.
```yaml
ports:
- 5000:5000
```

Run `docker-compose up --build` and after a while the app should be available on localhost:5000 or at the specified host (when using traefik).

# External APIs:
- http://positionstack.com
- https://openrouteservice.org/