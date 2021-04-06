from .sensors.cpu       import Cpu
from .sensors.raspCam   import RaspCam 
from .sensors.system    import System 
from .mqtt              import Mqtt
from .packetdt          import Packet 
from .sensor            import SensorManager
from .sensordt          import Sensorout
from .types             import hostName
from .configdt          import Devconf


def main(configPath: str):
    with open(configPath, "r") as f:
        devConf = Devconf().from_json(f.read())
    
    cpuSensor = Cpu(devConf.sensor_conf.cpu)
    camSensor = RaspCam(devConf.sensor_conf.rasp_cam)
    systemSensor = System(devConf.sensor_conf.system)
    manager = SensorManager()
    manager += cpuSensor
    manager += camSensor
    manager += systemSensor
    
    conn = Mqtt(hostName,
                devConf.mqtt_host,
                devConf.mqtt_port,
                devConf.mqtt_user,
                devConf.mqtt_pass,
                cleanSession=True)
    
    def cb(c,u,fl,rc):
        print('connected', flush=True)
        p = Packet()
        p.uid = hostName
        p.out = manager.retrieveAllData()
        
        c.publish("node/" + hostName,
                  p.SerializeToString(), 
                  qos=1,
                  retain=False)
        c.disconnect()
        
    conn.registerOnConnectCallback(cb)
    
    with conn.connect() as c:
        c.loop_forever()
