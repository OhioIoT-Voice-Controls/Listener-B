# Listener B<a href="https://www.ohioiot.com"><img src="https://www.ohioiot.com/logo_150.jpg" width="40" ></a>

##### [(back to the Voice Controls organization page)](https://github.com/OhioIoT-Voice-Controls)

This is a container implementation of our Vosk listener, with some flexibility to create your own custom commands.  The `docker-compose.yml` will spin up a Vosk listener and an MQTT broker, and link the listener to `commands.py` so you can edit the commands.  When you speak one of the defined commands, the listener send an MQTT message with topic `voice/command` where the payload is the command that is maps to your speech in commands.py.  

You can see this repo in use in the OhioIoT YouTube video [3 Steps To Your Custom Voice Control](https://youtu.be/_ERvoHMBDac).

## Installation
Plug a USB microphone into a Raspberry Pi that has Docker and Docker Compose installed.  SSH into the Raspberry Pi and run the following commands:
```
git clone https://github.com/OhioIoT-Voice-Controls/Listener-B.git listener_b
cd listener_b
rm listener.py README.md
nano commands.py
```
Edit the `commands.py` to define your own customer commands.  Inside `commands.py`, they keys (the values before the colon) are the strings of spoken words that you will say to fire the command.  The values after the colon are what will be send when your spoken words are recognized as commands.
```
docker compose up
```
When you see the log `listening...`, it means your listener is up and listening.  At this point, speak one of the commands that you defined.  If Vosk successfully catches it, an MQTT message will go out to the broker.  Once you confirm the IP address of your Raspberry Pi, you can connect any other device to the Mosquitto broker, exposed on port 1883.  Your connected devices can subscribe to `voice/command` and hear what you are saying in the incoming message payloads.

The `listener.py` in this repo is just an artifact, here for reference only.  You cannot run this file in this root directly with its current configuration.  To witness this file running inside the container on the Raspberry Pi, when the container is running, type:
```
docker exec -it listener sh
```
And then, when inside the Listener container (`# `):
```
cd /app
ls -la
cat listener.py
```

## Links
- [OhioIoT YouTube Channel](https://www.youtube.com/@ohioiot) - Agenda free tutorials showing you how to get started in IoT
- [OhioIoT GitHub Index](https://github.com/OhioIoT-Examples) - The central index of code examples available on GitHub

## About
<a href="https://www.ohioiot.com"><img src="https://www.ohioiot.com/logo_150.jpg" width="40" ></a>

*OhioIoT is an IoT platform designed for small-scale IoT projects.  For more, check out our website at [www.OhioIoT.com](https://www.ohioiot.com).*

