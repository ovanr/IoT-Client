from typing            import List, Union, Dict

hostName = ""
with open("/etc/hostname", "r") as f:
    hostName = f.read().replace("\n", "")

