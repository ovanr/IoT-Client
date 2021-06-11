# IoT-Client

A IoT-Client app that communicates with a server running [IoT-Server](https://github.com/ovanr/IoT-Server). 
It ideally runs on Raspberry devices and will fetch data from sensors such
as a Camera or a CPU Temperature sensor and will send them to a broker using
MQTT.
It will additionally check for any commands that it has been requested to execute.

## Architecture

![Architecture Diagram](https://github.com/ovanr/IoT-Server/raw/main/architecture.png)

## Installation

1. `git submodule update --init --recursive fake_rpi`
2. `python -m venv .`
3. `source bin/activate`
4. `cd fake_rpi`
5. `poetry install`
6. `pip3 install -r requirementsWithoutFakeRpi.txt`
7. Update config file with credentials: `vim iotClient.conf`

For development you might want to use the fake_rpi project so:

8. Change any picamera references to fake_rpi.picamera
```
cd ..
sed -i -E -e 's/from(\s)*picamera/from\1fake_rpi.picamera/g' iotClient/sensors/raspCam.py 
```

For production instead use the actual picamera module:

8. Change picamera references to point to non-mock module
```
sed -i -E -e 's/from(\s)*fake_rpi.picamera/from\1picamera/g' iotClient/sensors/raspCam.py 
```

## Usage

Start app with: 

`python3 app.py iotClient.conf`

## Notice

This program was developed for the [Kamposnet](https://kampos.eu/) Research Project 
