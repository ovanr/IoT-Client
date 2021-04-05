###############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import numpy as np  # type: ignore
# import platform
from .wrappers import printf
from .Base import Base
from typing import Optional, Tuple

class BGR(object):
    """Fake class"""

    @printf
    def __init__(self, sz):
        # constructor
        self.array = np.random.rand(*sz)

    @printf
    def truncate(self, num):
        # refreshes the fake image
        self.array = np.random.rand(*self.array.shape)


# class picamera(object):
#     """Fake class"""
class PiCamera(Base):
    """Fake class"""
    resolution = (0, 0)

    def __init__(self, resolution=None):
        # empty constructor
        # print('WARNING: Fake_RPi PiCamera on {}'.format(platform.system().lower()))
        Base.__init__(self, self.__class__)
        
        # default values as in picamera lib
        self.sharpness: int = 0
        self.contrast: int = 0
        self.brightness: int = 50
        self.saturation: int = 0
        self.iso: int = 0 # auto
        self.video_stabilization: bool = False
        self.exposure_compensation: int = 0
        self.exposure_mode: str = 'auto'
        self.meter_mode: str = 'average'
        self.awb_mode: str = 'auto'
        self.image_effect: str = 'none'
        
        # color_effects is an optional tuple
        # of two integers with a range 0-255 inclusive
        self.color_effects: Optional[Tuple[int,int]] = None
        self.rotation: int = 0
        self.hflip: bool = False
        self.vflip: bool = False
        self.zoom: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0)

    def __enter__(self):
        return self
    
    def start_preview(self, 
                      resolution=None, 
                      layer=2, 
                      alpha=255,
                      fullscreen=True, 
                      window=None, 
                      crop=None, 
                      rotation=0, 
                      vflip=False,
                      hflip=False, 
                      anamorphic=False):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        # this does nothing
        pass

    @printf
    def capture(self, 
                output, 
                format=None, 
                use_video_port=False, 
                resize=None, 
                splitter_port=0, 
                **options):
        if hasattr(output, "write") and callable(getattr(output, 'write')):
            output.write(b'deadbeef')
        elif isinstance(output, str):
            with open(output, "w") as f:
                f.write(b'deadbeef')

class array(object):
    """Fake class"""

    @staticmethod
    def PiRGBArray(cam, size):
        return BGR(size)
