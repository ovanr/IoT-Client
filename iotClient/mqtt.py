import paho.mqtt.client as mqtt

from typing     import List, Dict, Iterator, Callable, Optional
from contextlib import contextmanager 

from .misc      import callMany

MqttOnConnectCb = Callable[[mqtt.Client, None, Dict, int], None] 
MqttOnMessageCb = Callable[[mqtt.Client, None, mqtt.MQTTMessage], None] 

class Mqtt(mqtt.Client):
    onConnectCbs: List[MqttOnConnectCb] 
    onMessageCbs: List[MqttOnMessageCb]

    def __init__(self,
                 clientId: str,
                 mqttHost: str, 
                 mqttPort: int = 1883, 
                 mqttUser: Optional[str] = None, 
                 mqttPass: Optional[str] = None, 
                 cleanSession: bool = True):
        self.mqttHost = mqttHost 
        self.mqttPort = mqttPort 
        self.mqttUser = mqttUser 
        self.mqttPass = mqttPass 
        self.onConnectCbs = []
        self.onMessageCbs = []

        super().__init__(client_id=clientId, 
                         clean_session=cleanSession, 
                         protocol=mqtt.MQTTv311)

    def registerOnConnectCallback(self, cb: MqttOnConnectCb) -> int:
        self.onConnectCbs.append(cb)
        return len(self.onConnectCbs)

    def registerOnMessageCallback(self, cb: MqttOnMessageCb) -> int:
        self.onMessageCbs.append(cb)
        return len(self.onMessageCbs)
    
    @contextmanager
    def connect(self) -> Iterator[mqtt.Client]:
        super(Mqtt, type(self)).\
            on_connect.\
            fset(self, callMany(self.onConnectCbs)) # type: ignore
        
        super(Mqtt, type(self)).\
            on_message.\
            fset(self, callMany(self.onMessageCbs)) # type: ignore

        if self.mqttUser:
            super().username_pw_set(self.mqttUser, password=self.mqttPass)
        
        try:
            super().connect(self.mqttHost, self.mqttPort)
            yield super() 
        finally: 
            super().disconnect()
