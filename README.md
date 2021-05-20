# IoT-Client

A IoT-Client app that communicates with a server running [IoT-Server](https://github.com/ovanr/IoT-Server). 
It ideally runs on Raspberry devices and will fetch data from sensors such
as a Camera or a CPU Temperature sensor and will send them to a broker using
MQTT.
It will additionally check for any commands that it has been requested to execute.

## Architecture

![Architecture Diagram](https://github.com/ovanr/IoT-Server/raw/main/architecture.png)

## Installation

1. `pip3 install -r requirementsWithoutFakeRpi.txt`
2. Update config file with credentials: `vim iotClient.conf`
3. Change picamera references to point to non-mock module
```
sed -i -E -e 's/from(\s)*fake_rpi.picamera/from\1picamera/g' iotClient/sensors/raspCam.py 
```

For development you might want to build the forked fake_rpi project:
1. `cd fake_rpi`
2. `poetry install`
3. Change any picamera references to fake_rpi.picamera
```
cd ..
sed -i -E -e 's/from(\s)*picamera/from\1fake_rpi.picamera/g' iotClient/sensors/raspCam.py 
```

## Usage

Start app with: 

`python3 app.py iotClient.conf`

## Notice

This program was developed for the [Kamposnet](https://kampos.eu/) Research Project 
