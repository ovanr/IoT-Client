from __future__         import annotations

from ..sensor           import AbstractSensor
from ..sensordt         import Output 
from .raspcamdt         import Raspcamopt, Raspcamout, Encoding

from fake_rpi.picamera  import PiCamera
from time               import sleep
from io                 import BytesIO
from enum               import Enum

def getEnumName(enum: Enum):
    name = enum.name 
    if '_' in name:
        (_,name) = name.split('_')
    return name.lower()

class RaspCam(AbstractSensor):
    config: Raspcamopt

    def __init__(self, config: Raspcamopt):
        super().__init__("RaspCam")
        self.config = config
        self.cam = PiCamera(resolution="1080p")
        self.cam.rotation = config.rotation
        self.cam.vflip = config.vflip
        self.cam.hflip = config.hflip
        self.cam.contrast = config.contrast
        self.cam.sharpness = config.sharpness
        self.cam.brightness = config.brightness
        self.cam.saturation = config.saturation
        self.cam.exposure_mode = getEnumName(config.exposure)
        self.cam.awb_mode = getEnumName(config.awb)
        self.cam.image_effect = getEnumName(config.imxfx)
    
    def __enter__(self) -> RaspCam:
        self.cam.start_preview()
        # Camera warm-up time
        sleep(3)
        
        return self

    def __exit__(self) -> None:
        self.cam.close()
        
    def capture(self) -> bytes:
        print('capturing...')
        stream = BytesIO() 
        self.cam.capture(stream, 
                         format=getEnumName(self.config.encoding),
                         quality=self.config.quality)
        stream.seek(0)
        return stream.read()

    def retrieveData(self) -> Output:
        return Output(
            cam=Raspcamout(
                encoding=self.config.encoding,
                bin=self.capture()
            )
        )
