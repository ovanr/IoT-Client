from __future__         import annotations

from ..sensor           import AbstractSensor
from ..sensordt         import Output 
from .raspcamdt         import Raspcamopt, Raspcamout, Encoding
from .raspcamdt         import Exposure, Awb, Imxfx

from picamera  import PiCamera
from typing             import Iterator, Union, Optional
from time               import sleep
from io                 import BytesIO
from enum               import Enum
from contextlib         import contextmanager

def getEnumName(enum: Union[Enum,int], class_: Optional[type] = None):
    if isinstance(enum, int):
        name = class_(enum).name
    else:
        name = enum.name 
    
    if '_' in name:
        (_,name) = name.split('_')
    
    return name.lower()

class RaspCam(AbstractSensor):
    config: Raspcamopt

    def __init__(self, config: Raspcamopt):
        super().__init__("RaspCam")
        self.config = config
    
    @contextmanager 
    def camera(self) -> Iterator[PiCamera]:
        cam = PiCamera(resolution="1080p")
        cam.rotation = self.config.rotation
        cam.vflip = self.config.vflip
        cam.hflip = self.config.hflip
        cam.contrast = self.config.contrast
        cam.sharpness = self.config.sharpness
        cam.brightness = self.config.brightness
        cam.saturation = self.config.saturation
        cam.exposure_mode = getEnumName(self.config.exposure, Exposure)
        cam.awb_mode = getEnumName(self.config.awb, Awb)
        cam.image_effect = getEnumName(self.config.imxfx, Imxfx)
        
        cam.start_preview()
        # Camera warm-up time
        sleep(3)

        try: 
            yield cam 
        finally:
            cam.close()

    def capture(self) -> bytes:
        print('capturing...')
        stream = BytesIO() 
        with self.camera() as cam:
            cam.capture(stream, 
                        format=getEnumName(self.config.encoding, Encoding),
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
