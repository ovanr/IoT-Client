from .sensors.cpu       import Cpu
from .sensors.raspCam   import RaspCam 
from .sensors.system    import System 
from .sensors.generic   import Generic 
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
from functools          import partial
import threading

hostName = getHostName() 
print("HostName:", hostName)

def main(configPath: str):
    config = readConf(configPath)
    conn   = createConn(config)
    mqttDo(configPath, config, conn)

def readConf(configPath) -> Devconf:
    with open(configPath, "r") as f:
        return Devconf().from_json(f.read())

def createConn(config: Devconf) -> Mqtt:
    return Mqtt(hostName,
                config.mqtt_host,
                1883,
                config.mqtt_user,
                config.mqtt_pass,
                cleanSession=False)

def parseCmdPacket(configPath: str, origConf: Devconf, payload: bytes) -> int:
    cmdManager = CommandManager()
    cmdManager += ConfUpdate(configPath, origConf)
    cmdManager += Reboot()

    p = Packet().parse(payload)
    print("Received packet:", p)
    return cmdManager.performCommands(p.cmds)

def createNewSensorOutPacket(devConf: Devconf) -> Packet:
    sensorManager = SensorManager()
    sensorManager += RaspCam(devConf.sensor_conf.rasp_cam)
    sensorManager += Cpu(devConf.sensor_conf.cpu)
    sensorManager += System(devConf.sensor_conf.system)
    sensorManager += Generic(devConf.sensor_conf.generic)

    return Packet(uid=hostName,
                  out=sensorManager.retrieveAllData())

def onMsgReceive(lock, configPath, config, conn, _,msg):
    print('connected', flush=True)
    with lock:
        print("Commands performed:", 
               parseCmdPacket(configPath, config, msg.payload))

def onConnectSub(topic, conn, *args, **kwargs):
    print("Subscribed: ",
           topic[0],
           conn.subscribe(topic[0], topic[1]))

def mqttDo(configPath: str, config: Devconf, conn: Mqtt):
    lock = threading.Lock()
    topic = ("cmd/" + hostName, 1)
    
    conn.registerOnMessageCallback(
        partial(onMsgReceive, lock, configPath, config)
    )
    
    conn.registerOnConnectCallback(
        partial(onConnectSub, topic)
    )

    with conn.connect() as c:
        # wait 5 seconds for any receiving commands 
        sleep(5)
        
        with lock:
            # config might have been updated so re-read
            devConf = readConf(configPath)
            print("Config read as: ", devConf)

            pck = createNewSensorOutPacket(devConf)
            # print(pck)  
            c.publish("data/" + hostName,
                      pck.SerializeToString(), 
                      qos=1,
                      retain=False)
