from .sensors.cpu       import Cpu
from .sensors.raspCam   import RaspCam 
from .sensors.system    import System 
from .cmd.reboot        import Reboot 
from .cmd.confUpdate    import ConfUpdate 
from .mqtt              import Mqtt
from .packetdt          import Packet 
from .sensor            import SensorManager
from .sensordt          import Sensorout
from .command           import CommandManager
from .sensordt          import Sensorout
from .misc              import getHostName
from .configdt          import Devconf

from time               import sleep
import threading

hostName = getHostName() 

def main(configPath: str):
    mqttReceive(configPath)
    mqttSend(configPath)

def mqttReceive(configPath: str):
    with open(configPath, "r") as f:
        devConf = Devconf().from_json(f.read())
    
    cmdManager = CommandManager() 
    
    cmdManager += Reboot()
    cmdManager += ConfUpdate(configPath)
    
    lock = threading.Lock()

    # start new connection with cleanSession off
    # in order to receive previously missed msgs
    conn = Mqtt(hostName,
                devConf.mqtt_host,
                1884,
                devConf.mqtt_user,
                devConf.mqtt_pass,
                cleanSession=False)

    def cb(c,_,m):
        with lock:
            print('connected', flush=True)
            p = Packet().parse(m.payload)
            cmdManager.performCommands(p.cmds)

        # disconnect from connection as soon as cmds are performed 
        c.disconnect()
        
    conn.registerOnMessageCallback(cb)
    
    with conn.connect() as c:
        sleep(5)   
        with lock: 
            c.disconnect()

def mqttSend(configPath: str):
    with open(configPath, "r") as f:
        devConf = Devconf().from_json(f.read())

    sensorManager = SensorManager()
    sensorManager += Cpu(devConf.sensor_conf.cpu)
    sensorManager += RaspCam(devConf.sensor_conf.rasp_cam)
    sensorManager += System(devConf.sensor_conf.system)
    
    conn = Mqtt(hostName,
                devConf.mqtt_host,
                1883,
                devConf.mqtt_user,
                devConf.mqtt_pass,
                cleanSession=True)
    
    def cb(c,_,fl,rc):
        print('connected', flush=True)
        p = Packet()
        p.uid = hostName
        p.out = sensorManager.retrieveAllData()
        
        c.publish("node/" + hostName,
                  p.SerializeToString(), 
                  qos=1,
                  retain=False)

        # disconnect from connection as soon as msg is sent 
        c.disconnect()
        
    conn.registerOnConnectCallback(cb)
    
    with conn.connect() as c:
        c.loop_forever()
