# Listener B<a href="https://www.ohioiot.com"><img src="https://www.ohioiot.com/logo_150.jpg" width="40" ></a>

##### [(back to the Voice Controls organization page)](https://github.com/OhioIoT-Voice-Controls)

This is a container implementation of our Vosk listener, with some flexibility to create your own custom commands.  The `docker-compose.yml` will spin up a Vosk listener and an MQTT broker, and link the listener to `commands.py` so you can edit the commands.  When you speak one of the defined commands, the listener send an MQTT message with topic `voice/command` where the payload is the command that is maps to your speech in commands.py.  

You can see this repo in use in the OhioIoT YouTube video [3 Steps To Your Custom Voice Control](https://youtu.be/_ERvoHMBDac).

## Installation

*** See the Security Recommendations below before you run these commands ***

Plug a USB microphone into a Raspberry Pi that has Docker and Docker Compose installed.  SSH into the Raspberry Pi and run the following commands.  When the command list pops up, edit your commands as you choose, and exit with `[CTRL]-x, y, [ENTER]`:
```
git clone https://github.com/OhioIoT-Voice-Controls/Listener-B.git listener_b
cd listener_b
rm listener.py README.md
nano commands.py
docker compose up
```

When you see `listening...` in the logs, it means your listener is up and ready.  At this point, speak one of the commands that you defined.  If Vosk successfully catches it (it usually does), an MQTT message will go out to the broker.  With the IP address of your Raspberry Pi, you can connect any other device to the Mosquitto broker, exposed at 1883.  Your connected devices can subscribe to `voice/command` and hear what you are saying in the incoming message payloads.

When you are comfortable that everything is in order, start running the container in the background:
```
docker compose up -d
```

To edit the commands again, try:
```
nano ~/listener_b/commands.py
docker restart listener
```
When editing commands, the keys (the values before the colon) are the strings of spoken words that you will say to fire the command.  The values after the colon are what will be send when your spoken words are recognized as commands:
```
      this is what you speak   
                |        this is the command that goes out
                |                    |
     "close the garage door": "garage_close"

```

To tear this down if you don't want it:
```
cd ~/listener_b
docker compose down
cd ..
rm -rf listener_b
```
## Security Recommendation
You probably shouldn't run someone else's Docker container if you don't trust it.  Rather than trust, you can verify what is in the container with the following steps.  If this doesn't resolve all questions, you can just skip straight to Listener C ([Listener C Build](https://github.com/OhioIoT-Voice-Controls/Listener-C-Build) and [Listener C](https://github.com/OhioIoT-Voice-Controls/Listener-C)), where you build the container image yourself, so any security concerns should be assuaged:
```
docker run -d --network=none --name=listener lvincek/listener_b:latest
docker inspect listener
```
Look at the result from the `inspect` command.  You will notice that the working directort is /app, and the command that is run is `python -u listener.py`.  
```
            ],
            "Cmd": [
                "python",
                "-u",
                "listener.py"                                 <-- look for this
            ],
            "Image": "lvincek/listener_b:latest",
            "Volumes": null,
            "WorkingDir": "/app",                             <-- look for this
            "Entrypoint": null,

```
With that, you can step into the running container with:
```
docker exec -it listener sh
```
And then, print the file on your screen, and you will see that it is in fact the listener.py that you see in this repo.
```
cat /app/listener.py
```
When you are done, type `exit` to exit the container, and then `docker rm -f listener` to stop and remove the running container.



## Links
- [Listener A](https://github.com/OhioIoT-Voice-Controls/Listener-A)
- [Listener C Build](https://github.com/OhioIoT-Voice-Controls/Listener-C-Build)
- [Listener C](https://github.com/OhioIoT-Voice-Controls/Listener-C)
- [OhioIoT YouTube Channel](https://www.youtube.com/@ohioiot) - Agenda free tutorials showing you how to get started in IoT
- [OhioIoT GitHub Index](https://github.com/OhioIoT-Examples) - The central index of code examples available on GitHub

## About
<a href="https://www.ohioiot.com"><img src="https://www.ohioiot.com/logo_150.jpg" width="40" ></a>

*OhioIoT is an IoT platform designed for small-scale IoT projects.  For more, check out our website at [www.OhioIoT.com](https://www.ohioiot.com).*

