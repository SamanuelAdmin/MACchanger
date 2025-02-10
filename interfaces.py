import subprocess
import psutil
import re
from faker import Faker
import socket


fake = Faker()


class Interface:
    def __init__(self, name, mac, localIp):
        self.name = name
        self.mac = mac
        self.localIp = localIp

    def __str__(self):
        return f'{self.name} -> {self.mac} [{self.localIp}]'


def isValidMac(mac: str) -> bool:
    mac = mac.replace('-', ':').lower()
    return re.match(r"^([0-9A-Fa-f]{2}([-:])?){5}[0-9A-Fa-f]{2}$", mac)




def all():
    result = {}

    for ifaceName, ifaceInfo in psutil.net_if_addrs().items():
        ifaceMac = next((addr.address for addr in ifaceInfo if addr.family == psutil.AF_LINK), None)
        ifaceIp = next((addr.address for addr in ifaceInfo if addr.family == socket.AF_INET), None)

        if not isValidMac(ifaceMac): continue

        result[ifaceName] = Interface(ifaceName, ifaceMac, ifaceIp)

    return result

def getRandomMac() -> str: return fake.mac_address()

def setInterfaceMac(iface, mac): # from https://github.com/feross/SpoofMAC/blob/master/spoofmac/interface.py#L110
    print('"' + iface, '" -> ', mac)
    subprocess.call(f"ip link set {iface} down".split())
    subprocess.call(f"ip link set {iface} address {mac}".split())
    subprocess.call(f"ip link set {iface} up".split())



def test():
    for iface in psutil.net_if_addrs().items():
        print(iface)

if __name__ == '__main__': test()