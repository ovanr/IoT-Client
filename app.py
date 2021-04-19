#!/bin/env python3

from sys                import argv
from iotClient.main     import main


if len(argv) >= 2:
    conf = argv[1]
else:
    conf = "/etc/default/iotClient.conf"
    
exit(main(conf))
